import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import altair as alt

# ----------------------------
# Color Palette
# ----------------------------
BLACK = "#222831"
GREY = "#393E46"
DARKBEIGE = "#948979"
BEIGE = "#DFD0B8"

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    page_icon=":bar_chart:"
)

# ----------------------------
# Database Connection
# ----------------------------
warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a/duckdb_sample"
engine = create_engine(warehouse, client_encoding='utf8')
connection = engine.connect()

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM sales_data_duckdb;"
    result = connection.execute(text(query))
    return pd.DataFrame(result.mappings().all())

df = load_data()
df['Sales'] = df['Price Each'] * df['Quantity Ordered']
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Date'] = df['Order Date'].dt.date

# ----------------------------
# Title
# ----------------------------
st.markdown(f"""
    <h1 style='color:{BLACK}; margin-bottom: 0;'>📊 Simple Sales Dashboard</h1>
    <p style='color:{GREY}; font-size:16px;'>A clean overview of sales performance.</p>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------
# Chart 1: Total Sales Over Time
# ----------------------------
st.subheader("📈 Total Sales Over Time")
sales_over_time = df.groupby('Date')['Sales'].sum().reset_index()
line_chart = alt.Chart(sales_over_time).mark_line(color=DARKBEIGE).encode(
    x=alt.X('Date:T', title="Date"),
    y=alt.Y('Sales:Q', title="Total Sales")
).properties(
    height=350,
    width='container'
)
st.altair_chart(line_chart, use_container_width=True)

st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)

# ----------------------------
# Chart 2: Sales by Product
# ----------------------------
st.subheader("📦 Sales by Product")
sales_by_product = df.groupby('Product')['Sales'].sum().reset_index()
bar_chart = alt.Chart(sales_by_product).mark_bar(color=BEIGE).encode(
    x=alt.X('Product:N', sort='-y', title="Product"),
    y=alt.Y('Sales:Q', title="Sales"),
    tooltip=['Product', 'Sales']
).properties(
    height=350,
    width='container'
)
st.altair_chart(bar_chart, use_container_width=True)

# ----------------------------
# Footer / Close
# ----------------------------
st.markdown(f"""
    <div style='margin-top: 3rem; padding-top: 1rem; border-top: 1px solid {GREY}; color: {GREY}; font-size: 14px;'>
        Designed with ❤️ using Streamlit and Altair | Theme by ChatGPT
    </div>
""", unsafe_allow_html=True)
