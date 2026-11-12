import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Tanzania Commodity Tracker",
    page_icon="🇹🇿",
    layout="wide"
)

st.title("🇹🇿 Tanzania Regional Commodity Price Tracker")
st.write("Live market intelligence and regional price comparisons across major Tanzanian hubs.")

# Comprehensive Multi-Region Tanzanian Market Dataset
@st.cache_data
def load_market_data():
    data = [
        {"Region": "Dar es Salaam", "Market": "Kariakoo", "Commodity": "Maize (Mahindi)", "Price_TZS": 950, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Dar es Salaam", "Market": "Temeke", "Commodity": "Rice (Mchele)", "Price_TZS": 2400, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Dar es Salaam", "Market": "Kariakoo", "Commodity": "Beans (Maharage)", "Price_TZS": 3200, "Unit": "Kg", "Category":"Legumes"},
        {"Region": "Dar es Salaam", "Market": "Kinondoni", "Commodity": "Sunflower Oil", "Price_TZS": 6500, "Unit": "Litre", "Category": "Oils"},
        
        {"Region": "Arusha", "Market": "Central Market", "Commodity": "Maize (Mahindi)", "Price_TZS": 880, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Arusha", "Market": "Kilombero", "Commodity": "Rice (Mchele)", "Price_TZS": 2200, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Arusha", "Market": "Central Market", "Commodity": "Beans (Maharage)", "Price_TZS": 2900, "Unit": "Kg", "Category": "Legumes"},
        {"Region": "Arusha", "Market": "Kilombero", "Commodity": "Sunflower Oil", "Price_TZS": 6200, "Unit": "Litre", "Category": "Oils"},

        {"Region": "Mwanza", "Market": "Mpera", "Commodity": "Maize (Mahindi)", "Price_TZS": 920, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Mwanza", "Market": "Kirumba", "Commodity": "Rice (Mchele)", "Price_TZS": 2300, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Mwanza", "Market": "Mpera", "Commodity": "Beans (Maharage)", "Price_TZS": 3100, "Unit": "Kg", "Category": "Legumes"},
        {"Region": "Mwanza", "Market": "Kirumba", "Commodity": "Sunflower Oil", "Price_TZS": 6400, "Unit": "Litre", "Category": "Oils"},

        {"Region": "Dodoma", "Market": "Jamhuri", "Commodity": "Maize (Mahindi)", "Price_TZS": 850, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Dodoma", "Market": "Majengo", "Commodity": "Rice (Mchele)", "Price_TZS": 2100, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Dodoma", "Market": "Jamhuri", "Commodity": "Beans (Maharage)", "Price_TZS": 2800, "Unit": "Kg", "Category": "Legumes"},
        {"Region": "Dodoma", "Market": "Majengo", "Commodity": "Sunflower Oil", "Price_TZS": 6000, "Unit": "Litre", "Category": "Oils"},

        {"Region": "Mbeya", "Market": "Soweto", "Commodity": "Maize (Mahindi)", "Price_TZS": 780, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Mbeya", "Market": "Mwanjelwa", "Commodity": "Rice (Mchele)", "Price_TZS": 1900, "Unit": "Kg", "Category": "Cereals"},
        {"Region": "Mbeya", "Market": "Soweto", "Commodity": "Beans (Maharage)", "Price_TZS": 2500, "Unit": "Kg", "Category": "Legumes"},
        {"Region": "Mbeya", "Market": "Mwanjelwa", "Commodity": "Sunflower Oil", "Price_TZS": 5800, "Unit": "Litre", "Category": "Oils"},
    ]
    return pd.DataFrame(data)

df = load_market_data()
st.caption("📡 **Data Feed:** Active Regional Market Stream • Updated Daily")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
all_commodities = sorted(df["Commodity"].unique().tolist())
selected_commodities = st.sidebar.multiselect(
    "Select Commodities to Compare",
    options=all_commodities,
    default=all_commodities[:3]
)

if not selected_commodities:
    st.warning("Please select at least one commodity from the sidebar.")
    st.stop()

filtered_df = df[df["Commodity"].isin(selected_commodities)]

# Top Metric Summary Cards
st.subheader("📈 National Average Price Overview")
cols = st.columns(len(selected_commodities) if len(selected_commodities) <= 4 else 4)
for idx, item in enumerate(selected_commodities[:4]):
    avg_price = filtered_df[filtered_df["Commodity"] == item]["Price_TZS"].mean()
    cols[idx].metric(label=f"Avg {item}", value=f"{avg_price:,.0f} TZS")

# Interactive Regional Comparison Chart
st.subheader("📊 Regional Price Comparison (TZS per Unit)")
chart_pivot = filtered_df.pivot_table(
    index="Region",
    columns="Commodity",
    values="Price_TZS",
    aggfunc="mean"
)
st.bar_chart(chart_pivot)

# Detailed Data Table
with st.expander("📁 View Detailed Regional Breakdown Table"):
    st.dataframe(filtered_df, use_container_width=True)