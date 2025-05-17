import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import altair as alt

# Database connection
warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a/duckdb_sample"
engine = create_engine(warehouse, client_encoding='utf8')
connection = engine.connect()

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM sales_data_duckdb;"
    result = connection.execute(text(query))
    return pd.DataFrame(result.mappings().all())

df = load_data()

# Preprocessing
df['Sales'] = df['Price Each'] * df['Quantity Ordered']
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Date'] = df['Order Date'].dt.date

st.title("Simple Sales Dashboard")

# Total Sales Over Time - Line Chart
st.subheader("Total Sales Over Time")
sales_over_time = df.groupby('Date')['Sales'].sum().reset_index()
line_chart = alt.Chart(sales_over_time).mark_line().encode(
    x='Date:T',
    y='Sales:Q'
).properties(height=300)
st.altair_chart(line_chart, use_container_width=True)

# Sales by Product - Bar Chart
st.subheader("Sales by Product")
sales_by_product = df.groupby('Product')['Sales'].sum().reset_index()
bar_chart = alt.Chart(sales_by_product).mark_bar().encode(
    x=alt.X('Product:N', sort='-y'),
    y='Sales:Q'
).properties(height=300)
st.altair_chart(bar_chart, use_container_width=True)
