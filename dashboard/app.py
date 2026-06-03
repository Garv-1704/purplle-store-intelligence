import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide"
)

st.title("🛍️ Purplle AI Retail Intelligence Platform")

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

            camera = event.get("camera_id", event.get("camera"))

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

if entries >= transactions and entries > 0:
    conversion_rate = (transactions / entries) * 100
    conversion_display = f"{conversion_rate:.1f}%"
else:
    conversion_display = "Insufficient Data"

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
category_revenue = (
    sales_df.groupby("dep_name")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

category_percent = (
    category_revenue / revenue * 100
).round(1)
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
col5.metric("Conversion Rate", conversion_display)
st.divider()

st.subheader("Sales Funnel")

f1, f2, f3 = st.columns(3)

f1.metric("Visitors", entries)
f2.metric("Transactions", transactions)
f3.metric("Revenue", f"₹{revenue:,.0f}")

# =====================
# INSIGHTS
# =====================

st.divider()

st.subheader("Retail Intelligence Insights")

c1, c2 = st.columns(2)

c1.metric("Top Brand", top_brand)
c2.metric("Top Category", top_category)

st.divider()

st.subheader("AI Recommendations")

st.success(
    "Makeup category contributes the majority of store revenue. "
    "Consider increasing shelf visibility and promotional offers."
)

st.info(
    "Faces Canada is the top-performing brand. "
    "Allocate additional inventory to avoid stockouts."
)

st.warning(
    "Monitor billing zone traffic during peak hours to reduce waiting time."
)
st.divider()

st.subheader("Revenue Contribution by Category")

c1, c2, c3, c4, c5 = st.columns(5)

categories = category_percent.head(5)

c1.metric(categories.index[0].title(), f"{categories.iloc[0]}%")
c2.metric(categories.index[1].title(), f"{categories.iloc[1]}%")
c3.metric(categories.index[2].title(), f"{categories.iloc[2]}%")
c4.metric(categories.index[3].title(), f"{categories.iloc[3]}%")
c5.metric(categories.index[4].title(), f"{categories.iloc[4]}%")

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

st.subheader("Zone Analytics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Store Floor", camera_counts["CAM_1"])
c2.metric("Makeup Zone", camera_counts["CAM_2"])
c3.metric("Entrance", camera_counts["CAM_3"])
c4.metric("Storage Room", camera_counts["CAM_4"])
c5.metric("Billing Zone", camera_counts["CAM_5"])

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