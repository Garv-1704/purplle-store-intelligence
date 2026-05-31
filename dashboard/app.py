import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Store Intelligence", layout="wide")

st.title("🛍️ Purplle Store Intelligence")

entries = 0
exits = 0

try:
    with open("events.jsonl", "r") as f:
        for line in f:
            event = json.loads(line)

            if event["event_type"] == "ENTRY":
                entries += 1

            if event["event_type"] == "EXIT":
                exits += 1

except FileNotFoundError:
    pass

active_visitors = entries - exits

col1, col2, col3 = st.columns(3)

col1.metric("Total Entries", entries)
col2.metric("Total Exits", exits)
col3.metric("Active Visitors", active_visitors)

st.divider()

st.subheader("Recent Events")

try:
    df = pd.read_json("events.jsonl", lines=True)
    st.dataframe(df.tail(20), use_container_width=True)
except:
    st.info("No events found")