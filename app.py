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
        
        # Extract records depending on JSON structure
        records = payload.get("data", payload) if isinstance(payload, dict) else payload
        df = pd.DataFrame(records)
        
        if not df.empty:
            return df, "Live API (Nukta AI)"
    except Exception:
        pass  # Fall back smoothly to local CSV if API is unreachable

    # Fallback to local CSV
    df = pd.read_csv("commodities.csv")
    return df, "Local Backup Dataset (CSV)"

# Load the data
df, data_source = load_live_data()

# Show data source status badge
st.caption(f"📡 **Data Source:** {data_source} • Auto-refreshes every 10 minutes")

# Safely clean and flatten columns in case API returns nested objects (dicts/lists)
for col in df.columns:
    # If a column contains dictionaries, extract a text field (e.g., 'name' or 'title')
    if df[col].apply(lambda x: isinstance(x, dict)).any():
        df[col] = df[col].apply(lambda x: x.get('name', x.get('title', str(x))) if isinstance(x, dict) else str(x))
    else:
        df[col] = df[col].astype(str)

# Dynamically detect column names
commodity_col = next((c for c in df.columns if c.lower() in ["commodity", "name", "bidhaa", "item"]), df.columns[0])
region_col = next((c for c in df.columns if c.lower() in ["region", "location", "market", "city"]), None)
price_col = next((c for c in df.columns if "price" in c.lower() or "bei" in c.lower()), None)

# Ensure commodity column is purely string and safe for sorting
df[commodity_col] = df[commodity_col].fillna("Unknown").astype(str)

# Sidebar Multi-Select Filter
st.sidebar.header("🔍 Filter Options")
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

# Display Top Metrics
if price_col:
    filtered_df[price_col] = pd.to_numeric(filtered_df[price_col], errors="coerce")
    cols = st.columns(len(selected_commodities))
    for idx, item in enumerate(selected_commodities):
        avg_val = filtered_df[filtered_df[commodity_col] == item][price_col].mean()
        if pd.notna(avg_val):
            cols[idx].metric(label=f"Avg {item}", value=f"{avg_val:,.0f} TZS")
        else:
            cols[idx].metric(label=f"Avg {item}", value="N/A")

# Interactive Chart
st.subheader("📊 Price Comparison Across Regions")
if region_col and price_col:
    chart_data = filtered_df.pivot_table(index=region_col, columns=commodity_col, values=price_col, aggfunc="mean")
    st.bar_chart(chart_data)
else:
    st.dataframe(filtered_df)

# Raw Data Table
with st.expander("📁 View Full Live Dataset"):
    st.dataframe(filtered_df, use_container_width=True)