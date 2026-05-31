import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide"
)

st.title("🛍️ Purplle Store Intelligence Dashboard")

# =====================
# EVENTS ANALYTICS
# =====================

entries = 0
exits = 0

camera_counts = {
    "CAM_1": 0,
    "CAM_2": 0,
    "CAM_3": 0,
    "CAM_4": 0,
    "CAM_5": 0
}

events = []

try:
    with open("events.jsonl", "r") as f:

        for line in f:

            event = json.loads(line)
            events.append(event)

            camera = event.get("camera")

            if camera in camera_counts:
                camera_counts[camera] += 1

            if event["event_type"] == "ENTRY":
                entries += 1

            if event["event_type"] == "EXIT":
                exits += 1

except FileNotFoundError:
    pass

active_visitors = entries - exits

# =====================
# SALES ANALYTICS
# =====================

sales_df = pd.read_csv(
    "sales_data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv"
)

revenue = sales_df["total_amount"].sum()
transactions = sales_df["invoice_number"].nunique()
units_sold = sales_df["qty"].sum()
abv = revenue / transactions

conversion_rate = (
    transactions / max(entries, 1)
) * 100

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

# =====================
# FOOTFALL
# =====================

st.subheader("Footfall Analytics")

col1, col2, col3 = st.columns(3)

col1.metric("Entries", entries)
col2.metric("Exits", exits)
col3.metric("Active Visitors", active_visitors)

# =====================
# SALES KPIs
# =====================

st.divider()

st.subheader("Sales Analytics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Revenue", f"₹{revenue:,.0f}")
col2.metric("Transactions", transactions)
col3.metric("Units Sold", int(units_sold))
col4.metric("Avg Bill Value", f"₹{abv:,.0f}")
col5.metric("Conversion Rate", f"{conversion_rate:.1f}%")

# =====================
# INSIGHTS
# =====================

st.divider()

st.subheader("Business Insights")

c1, c2 = st.columns(2)

c1.metric("Top Brand", top_brand)
c2.metric("Top Category", top_category)

# =====================
# TOP BRANDS CHART
# =====================

st.divider()

st.subheader("Top Brands")

brand_sales = (
    sales_df.groupby("brand_name")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    brand_sales,
    x="brand_name",
    y="total_amount",
    title="Top 10 Brands by Revenue"
)

fig1.update_layout(
    dragmode=False
)

fig1.update_xaxes(
    tickangle=-45
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    config={
        "scrollZoom": False
    }
)

# =====================
# TOP CATEGORIES CHART
# =====================

st.subheader("Top Categories")

category_sales = (
    sales_df.groupby("dep_name")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x="dep_name",
    y="total_amount",
    title="Revenue by Category"
)

fig2.update_layout(
    dragmode=False
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    config={
        "scrollZoom": False
    }
)

# =====================
# CAMERA EVENTS
# =====================

st.divider()

st.subheader("Camera-wise Events")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("CAM 1", camera_counts["CAM_1"])
c2.metric("CAM 2", camera_counts["CAM_2"])
c3.metric("CAM 3", camera_counts["CAM_3"])
c4.metric("CAM 4", camera_counts["CAM_4"])
c5.metric("CAM 5", camera_counts["CAM_5"])

# =====================
# EVENT TABLE
# =====================

st.divider()

st.subheader("Recent Events")

if len(events) > 0:
    event_df = pd.DataFrame(events)
    st.dataframe(
        event_df.tail(20),
        use_container_width=True
    )
else:
    st.info("No events available")