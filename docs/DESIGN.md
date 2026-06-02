# System Design

## Architecture Overview

The Purplle Retail Intelligence Platform combines computer vision, tracking, analytics, and business intelligence to provide actionable insights for retail stores.

### Pipeline

1. CCTV Camera Feeds (CAM 1–5)
2. YOLOv8 Person Detection
3. ByteTrack Multi-Object Tracking
4. Event Generation Engine
5. Retail Analytics Engine
6. FastAPI Intelligence Layer
7. Streamlit Dashboard

### Components

#### Detection Layer

YOLOv8 is used to detect customers from store camera feeds.

#### Tracking Layer

ByteTrack assigns unique visitor IDs and tracks movement across frames.

#### Event Layer

ENTRY and EXIT events are generated and stored in events.jsonl.

#### Analytics Layer

Sales data is processed using Pandas to generate revenue, transaction, brand, and category insights.

#### API Layer

FastAPI exposes metrics, funnel, zone analytics, insights, and anomaly endpoints.

#### Dashboard Layer

Streamlit provides visual analytics and business recommendations.
