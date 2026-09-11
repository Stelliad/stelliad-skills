> **Worked example, not a real system.** Acme Platform is fictional. This file
> is the companion to `example-readme.md` and shows what belongs outside a README
> once it passes 500 lines.

# Architecture: Acme Platform

This document covers the system design decisions, tradeoffs, and boundaries. The README covers how to run and deploy it, this covers why it's built this way.

## Design Principles

1. **Tenant isolation at the data layer.** Every query, every write, every read is scoped to a tenant. There is no "global" table scan that touches all tenants. Partition keys encode tenant ID.

2. **Hot path vs. cold path separation.** Real-time queries (dashboards, live counters) hit Redis. Historical queries (last 90 days, funnels, retention) hit S3 + Athena. They share ingestion but diverge at processing.

3. **Backpressure over data loss.** If the pipeline falls behind, we slow ingestion (HTTP 429) rather than drop events. Events are the customer's data: losing them silently is worse than being temporarily slow.

4. **Schema-on-read for events.** We don't enforce a rigid schema at ingestion beyond basic validation (required fields: `tenant_id`, `event_type`, `timestamp`). Customers define their own event properties. Schema enforcement happens at query time.

5. **No shared state between services.** Each service owns its data store. Services communicate via Kinesis (async) or HTTP (sync). No shared database connections.

## System Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Public Internet                              │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Ingestion Boundary                                                  │
│                                                                      │
│  ┌──────────────┐    ┌───────────────┐    ┌──────────────────────┐  │
│  │ API Gateway  │───▶│  Ingestion    │───▶│  Kinesis (3 shards)  │  │
│  │ (rate limit) │    │  Service      │    │  (event bus)         │  │
│  └──────────────┘    └───────────────┘    └──────────┬───────────┘  │
└──────────────────────────────────────────────────────┼──────────────┘
                                                       │
                    ┌──────────────────────────────────┼──────────────┐
                    │  Processing Boundary              │              │
                    │                                   │              │
                    │  ┌───────────────┐    ┌──────────┴───────────┐  │
                    │  │  Flink        │◀───┤  Kinesis Consumer    │  │
                    │  │  (real-time)  │    └──────────────────────┘  │
                    │  └───────┬───────┘                              │
                    │          │         ┌─────────────────────────┐  │
                    │          │         │  Spark (batch, 15-min)  │  │
                    │          │         └────────────┬────────────┘  │
                    │          │                      │               │
                    └──────────┼──────────────────────┼───────────────┘
                               │                      │
                    ┌──────────┼──────────────────────┼───────────────┐
                    │  Storage Boundary                │               │
                    │          ▼                       ▼               │
                    │  ┌──────────────┐    ┌────────────────────┐     │
                    │  │  Redis       │    │  S3 (Parquet)      │     │
                    │  │  (hot, 24h)  │    │  + Athena (cold)   │     │
                    │  └──────────────┘    └────────────────────┘     │
                    └─────────────────────────────────────────────────┘
                               │                      │
                    ┌──────────┼──────────────────────┼───────────────┐
                    │  Query Boundary                  │               │
                    │          ▼                       ▼               │
                    │  ┌─────────────────────────────────────────┐    │
                    │  │  Query API (FastAPI)                     │    │
                    │  │  routes: /realtime/* → Redis             │    │
                    │  │          /historical/* → Athena          │    │
                    │  │          /export/* → S3 presigned        │    │
                    │  └─────────────────────────────────────────┘    │
                    └─────────────────────────────────────────────────┘
```

## Key Decisions

### Why Kinesis over SQS for event transport

Events need ordering within a tenant (for session stitching) and fan-out to multiple consumers (real-time + batch + alerts). Kinesis gives us both, partition by tenant_id for ordering, multiple consumers reading the same stream independently. SQS would require separate queues per consumer and doesn't guarantee ordering without FIFO (which caps at 300 msg/s per group).

**Tradeoff:** Kinesis costs more at low volume. Below ~1K events/sec, SQS would be cheaper. We crossed that threshold at month 3.

### Why Redis for hot storage instead of DynamoDB

Real-time dashboard queries need sub-10ms reads on pre-aggregated counters (unique users in last 5 minutes, events per second, top pages). Redis sorted sets and HyperLogLog give us O(1) reads on these aggregates. DynamoDB could serve this but adds 5-15ms of consistent read latency and requires more complex key design for time-windowed aggregates.

**Tradeoff:** Redis is not durable. If the node dies, we lose the hot window (last 24h of aggregates). The batch pipeline backfills from S3 within 15 minutes. Acceptable for dashboard data, not acceptable if this were the source of truth.

### Why schema-on-read

Customers send wildly different event shapes. A marketing SaaS sends `{page_url, referrer, utm_source}`. A fintech sends `{transaction_id, amount, currency, merchant}`. Enforcing a universal schema would either be so loose it's useless or so strict it blocks onboarding.

Instead: we validate structure (required fields exist, timestamp is parseable, payload < 64KB) and let customers define dimensions at query time. The Query API resolves property paths dynamically.

**Tradeoff:** Query performance suffers on unindexed properties. We mitigate with materialized views for each tenant's top-10 queried dimensions (auto-detected from query patterns after 7 days).

### Why separate Flink and Spark instead of one pipeline

Different latency requirements demand different tools. Flink gives us sub-second windowed aggregates (live dashboard counters). Spark gives us efficient batch processing over hours/days of data (retention rollups, funnel calculations, cohort analysis).

Running both through Flink is possible but Spark is 3-4x cheaper per TB for batch workloads and handles backfills more gracefully.

**Tradeoff:** Two systems to maintain. We accept this because the operational complexity is isolated, each pipeline team owns their stack independently.

## Scaling Limits

| Component | Current ceiling | What breaks | Fix |
|-----------|----------------|-------------|-----|
| Kinesis | 3 shards = ~3K events/sec/shard | Hot shard on popular tenant | Shard splitting, tenant-aware partitioning |
| Redis | 64GB node | Memory exhaustion | Cluster mode (already configured, not yet needed) |
| Flink | 4 task slots | Checkpoint backpressure | Add task slots, increase parallelism |
| Athena | 100 concurrent queries | Queue timeout for heavy tenants | Workgroup isolation per tier |
| Ingestion ECS | 10 tasks (autoscale to 50) | Cold start on traffic spikes | Pre-warm pool for enterprise tenants |

**Current capacity:** ~50K events/sec sustained, ~120K burst (90-second window).

**Next bottleneck:** Kinesis shard limits for the top 3 tenants. Solution already designed (tenant-aware shard splitting) but not implemented, projected need in Q4.

## Data Model

### DynamoDB (tenants)

```
PK: TENANT#{tenant_id}
SK: CONFIG

Attributes:
  name, plan, api_key_hash, created_at, status,
  retention_days, rate_limit_per_sec, custom_dimensions[]
```

### Redis (hot aggregates)

```
Key pattern: {tenant_id}:{metric}:{window}:{dimension_value}
TTL: 24 hours (configurable per tenant)

Examples:
  acme:page_views:5m:2026-07-29T16:30    → 4,521
  acme:uniques:1h:2026-07-29T16:00       → HyperLogLog
  acme:top_pages:1h:2026-07-29T16:00     → Sorted Set
```

### S3 (cold storage)

```
Path: s3://platform-events/{tenant_id}/year={YYYY}/month={MM}/day={DD}/hour={HH}/{uuid}.parquet
Partitioned by: tenant_id, date, hour
Format: Parquet (Snappy compression)
Retention: per-tenant setting (default 90 days, enterprise unlimited)
```

## Security Boundaries

- **Tenant isolation:** Every query includes tenant_id in the predicate. No cross-tenant reads are possible at the storage layer (S3 prefixes, DynamoDB partition keys, Redis key prefixes all encode tenant).
- **API authentication:** HMAC-signed API keys with per-key rate limits and IP allowlists (enterprise tier).
- **Internal services:** mTLS between ECS services within the VPC. No public endpoints on processing or storage layers.
- **Encryption:** AES-256 at rest (S3, DynamoDB, Redis), TLS 1.3 in transit. Customer-managed KMS keys available on enterprise tier.
- **Audit:** All API calls logged to CloudTrail. All data access logged to a separate audit stream (7-year retention for compliance).

## Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Redis node crash | Live dashboards show stale data (up to 15 min) | Auto-failover to replica; batch pipeline backfills |
| Flink checkpoint failure | Aggregates may double-count during recovery window | Flink restores from last checkpoint; slight over-count for ~60s |
| Kinesis throttle | Ingestion returns 429 to clients | Clients retry with backoff; no data loss |
| S3 partition corruption | Historical queries return incomplete for affected hour | Re-process from Kinesis retention (24h) or backup |
| Athena timeout | Long-running queries fail | Retry with smaller time window; alert if recurring |

## Future Considerations

- **Multi-region:** Currently us-east-1 only. Enterprise customers asking for eu-west-1. Design supports it (tenant-level region assignment) but infrastructure isn't provisioned.
- **Real-time ML:** Anomaly detection on ingested events (currently runs daily in batch). Moving to Flink-based streaming inference is Q1 next year.
- **GraphQL API:** Some customers want flexible queries beyond our REST patterns. Evaluating: concern is query cost explosion without proper depth limiting.
