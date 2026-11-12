import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Tanzania Commodity Tracker", page_icon="🇹🇿", layout="centered")

# App Header
st.title("🇹🇿 Tanzania Local Market Commodity Tracker")
st.write("A real-time dashboard tracking regional food and fuel prices across Tanzania.")

# Load the data safely
try:
    df = pd.read_csv('commodities.csv')
    # Clean whitespace
    df['Region'] = df['Region'].str.strip()
    df['Commodity'] = df['Commodity'].str.strip()
except FileNotFoundError:
    st.error("Error: 'commodities.csv' file not found. Make sure it is in the same folder!")
    st.stop()

# Sidebar Filters for User Interactivity
st.sidebar.header("Filter Options")
selected_commodity = st.sidebar.selectbox("Select a Commodity", df['Commodity'].unique())

# Filter the data based on what the user picked
filtered_df = df[df['Commodity'] == selected_commodity]

# Display Metrics
avg_price = filtered_df['Price_TZS'].mean()
st.metric(label=f"Average Price for {selected_commodity}", value=f"{avg_price:,.0f} TZS")

# Display Interactive Chart
st.subheader(f"Regional Price Breakdown ({selected_commodity})")
st.bar_chart(filtered_df.set_index('Region')['Price_TZS'])

# Raw Data Expander
with st.expander("View Raw Data Table"):
    st.dataframe(df)

st.markdown("---")
st.markdown("*Built by a Tanzanian high school student exploring software engineering and data science.*")