import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("📦 E-commerce Sales Dashboard")

# Load data
df = pd.read_csv("cleaned_ecommerce_data.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar filters
st.sidebar.header("Filter Options")

region = st.sidebar.multiselect("Select Region:", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category:", options=df['Product Category'].unique(), default=df['Product Category'].unique())

# Apply filters
filtered_df = df[(df['Region'].isin(region)) & (df['Product Category'].isin(category))]

# KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
avg_delivery = filtered_df['Delivery Time (Days)'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("Total Profit", f"₹ {total_profit:,.0f}")
col3.metric("Avg Delivery Time", f"{avg_delivery:.2f} days")

# Monthly Sales Chart
monthly_sales = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order Date'] = monthly_sales['Order Date'].astype(str)

fig1 = px.line(monthly_sales, x='Order Date', y='Sales', title="Monthly Sales Trend")
st.plotly_chart(fig1)

# Sales by Category
fig2 = px.bar(filtered_df.groupby('Product Category')['Sales'].sum().reset_index(),
              x='Product Category', y='Sales', title="Sales by Category")
st.plotly_chart(fig2)

# Profit vs Discount
fig3 = px.scatter(filtered_df, x='Discount', y='Profit', color='Product Category', title="Discount vs Profit")
st.plotly_chart(fig3)

st.markdown("📊 *Data Source: Simulated Dataset | Built by Abhishek Kumar Soni*")
