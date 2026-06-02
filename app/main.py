from fastapi import FastAPI
import json
import pandas as pd

app = FastAPI(
    title="Purplle Retail Intelligence API"
)

# =====================
# HEALTH
# =====================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# =====================
# HOME
# =====================

@app.get("/")
def home():
    return {
        "status": "running"
    }

# =====================
# METRICS
# =====================

@app.get("/stores/1/metrics")
def metrics():

    entries = 0
    exits = 0

    try:

        with open("events.jsonl", "r") as f:

            for line in f:

                event = json.loads(line)

                if event["event_type"] == "ENTRY":
                    entries += 1

                elif event["event_type"] == "EXIT":
                    exits += 1

    except FileNotFoundError:
        pass

    active_visitors = entries - exits

    return {
        "store_id": "PURPLLE_BLR_001",
        "entries": entries,
        "exits": exits,
        "active_visitors": active_visitors
    }

# =====================
# FUNNEL
# =====================

@app.get("/stores/1/funnel")
def funnel():

    entries = 0

    try:

        with open("events.jsonl", "r") as f:

            for line in f:

                event = json.loads(line)

                if event["event_type"] == "ENTRY":
                    entries += 1

    except FileNotFoundError:
        pass

    try:

        sales_df = pd.read_csv(
            "sales_data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv"
        )

        transactions = sales_df["invoice_number"].nunique()

    except Exception:

        transactions = 0

    estimated_visitors = max(entries, transactions)
    conversion_rate = (
        (transactions / estimated_visitors) * 100
        if estimated_visitors > 0 else 0
        )

    return {
        "store_id": "PURPLLE_BLR_001",
        "entries": entries,
        "transactions": transactions,
        "conversion_rate": round(conversion_rate, 2)
    }

@app.get("/stores/1/zones")
def zones():

    zone_counts = {}

    try:

        with open("events.jsonl", "r") as f:

            for line in f:

                event = json.loads(line)

                zone = event.get("zone_id", "UNKNOWN")

                zone_counts[zone] = (
                    zone_counts.get(zone, 0) + 1
                )

    except FileNotFoundError:
        pass

    return {
        "store_id": "PURPLLE_BLR_001",
        "zones": zone_counts
    }


@app.get("/stores/1/insights")
def insights():

    sales_df = pd.read_csv(
        "sales_data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv"
    )

    top_brand = (
        sales_df.groupby("brand_name")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )

    top_category = (
        sales_df.groupby("dep_name")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )

    revenue = round(
        sales_df["total_amount"].sum(),
        2
    )

    return {
        "store_id": "PURPLLE_BLR_001",
        "top_brand": top_brand,
        "top_category": top_category,
        "revenue": revenue
    }



@app.get("/stores/1/anomalies")
def anomalies():

    anomalies = []

    try:

        with open("events.jsonl", "r") as f:

            events = [json.loads(line) for line in f]

        if len(events) < 5:

            anomalies.append(
                "Low visitor traffic detected"
            )

    except FileNotFoundError:

        anomalies.append(
            "No event data available"
        )

    return {
        "store_id": "PURPLLE_BLR_001",
        "anomalies": anomalies
    }