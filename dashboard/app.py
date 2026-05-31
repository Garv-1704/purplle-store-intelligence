import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide"
)

st.title("🛍️ Purplle Store Intelligence Dashboard")

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
    st.error("events.jsonl not found")

active_visitors = entries - exits

st.subheader("Store Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Entries", entries)
col2.metric("Total Exits", exits)
col3.metric("Active Visitors", active_visitors)

st.divider()

st.subheader("Camera-wise Events")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("CAM 1", camera_counts["CAM_1"])
c2.metric("CAM 2", camera_counts["CAM_2"])
c3.metric("CAM 3", camera_counts["CAM_3"])
c4.metric("CAM 4", camera_counts["CAM_4"])
c5.metric("CAM 5", camera_counts["CAM_5"])

st.divider()

st.subheader("Recent Events")

if len(events) > 0:
    df = pd.DataFrame(events)
    st.dataframe(df.tail(20), use_container_width=True)
else:
    st.info("No events available")