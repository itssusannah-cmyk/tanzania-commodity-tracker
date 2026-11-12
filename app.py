import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Tanzania Commodity Tracker", page_icon="🇹🇿", layout="wide")

st.title("🇹🇿 Tanzania Live Market Commodity Tracker")
st.write("Real-time tracking of crop and market prices across Tanzanian regions.")

# Fetch live data from Nukta AI Public Data API (caches for 10 minutes / 600s)
@st.cache_data(ttl=600)
def load_live_data():
    api_url = "https://ai.nukta.co.tz/api/commodities"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        payload = response.json()
        
        records = payload.get("data", payload) if isinstance(payload, dict) else payload
        df = pd.DataFrame(records)
        
        if not df.empty:
            return df, "Live API (Nukta AI)"
    except Exception:
        pass

    # Fallback to local CSV
    df = pd.read_csv("commodities.csv")
    return df, "Local Backup Dataset (CSV)"

df, data_source = load_live_data()
st.caption(f"📡 **Data Source:** {data_source} • Auto-refreshes every 10 minutes")

# Safely clean columns
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, dict)).any():
        df[col] = df[col].apply(lambda x: x.get('name', x.get('title', str(x))) if isinstance(x, dict) else str(x))
    else:
        df[col] = df[col].astype(str)

# Sidebar: Commodity Filter
st.sidebar.header("🔍 Filter Options")
commodity_col = next((c for c in df.columns if c.lower() in ["commodity", "name", "bidhaa", "item"]), df.columns[0])
df[commodity_col] = df[commodity_col].fillna("Unknown").astype(str)

all_commodities = sorted(df[commodity_col].dropna().unique().tolist())
selected_commodities = st.sidebar.multiselect(
    "Select Commodities to Compare",
    options=all_commodities,
    default=all_commodities[:3] if len(all_commodities) >= 3 else all_commodities
)

if not selected_commodities:
    st.warning("Please select at least one commodity from the sidebar.")
    st.stop()

filtered_df = df[df[commodity_col].isin(selected_commodities)]

# Sidebar: Manual Column Mapping for Charts (Guarantees graphs show up!)
st.sidebar.markdown("---")
st.sidebar.header("📊 Chart Configuration")
region_col = st.sidebar.selectbox("Select Region/Market Column", options=df.columns.tolist(), index=0)
price_col = st.sidebar.selectbox("Select Price Column", options=df.columns.tolist(), index=min(1, len(df.columns)-1))

# Convert price to numeric safely
filtered_df[price_col] = pd.to_numeric(filtered_df[price_col], errors="coerce")

# Display Top Metrics
cols = st.columns(len(selected_commodities) if len(selected_commodities) <= 4 else 4)
for idx, item in enumerate(selected_commodities[:4]):
    avg_val = filtered_df[filtered_df[commodity_col] == item][price_col].mean()
    if pd.notna(avg_val):
        cols[idx].metric(label=f"Avg {item}", value=f"{avg_val:,.0f} TZS")
    else:
        cols[idx].metric(label=f"Avg {item}", value="N/A")

# Interactive Chart
st.subheader("📊 Price Comparison Across Regions")
try:
    chart_data = filtered_df.pivot_table(index=region_col, columns=commodity_col, values=price_col, aggfunc="mean")
    st.bar_chart(chart_data)
except Exception:
    st.info("Showing raw table while chart is configuring:")
    st.dataframe(filtered_df)

# Raw Data Table
with st.expander("📁 View Full Dataset"):
    st.dataframe(filtered_df, use_container_width=True)