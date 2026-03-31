import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Load data
df = pd.read_csv("cleaned_sales.csv")
df.columns = df.columns.str.strip()

# Fix date column
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

# Sidebar navigation
st.sidebar.title("📊 Dashboard Menu")
page = st.sidebar.radio("Go to", ["Home", "Sales", "Products"])

# Sidebar filter
st.sidebar.header("Filters")
if 'category' in df.columns:
    category = st.sidebar.selectbox("Select Category", df['category'].unique())
    df = df[df['category'] == category]

# =========================
# 🏠 HOME PAGE
# =========================
if page == "Home":
    st.title("🛒 E-Commerce Dashboard")

    total_sales = df['Unit Price'].sum()
    total_orders = df['Order ID'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("💰 Total Sales", f"₹{total_sales}")
    col2.metric("📦 Total Orders", total_orders)

    st.divider()

    # Monthly sales chart
    if 'Month' in df.columns:
        st.subheader("📅 Monthly Sales")
        monthly_sales = df.groupby('Month')['Unit Price'].sum()
        st.line_chart(monthly_sales)

# =========================
# 📈 SALES PAGE
# =========================
elif page == "Sales":
    st.title("📈 Sales Analysis")

    col1, col2 = st.columns(2)

    # Category sales
    if 'category' in df.columns:
        category_sales = df.groupby('category')['Unit Price'].sum().reset_index()
        col1.subheader("Category Sales")
        col1.bar_chart(category_sales.set_index('category'))

    # Daily sales trend
    if 'Order Date' in df.columns:
        trend = df.groupby('Order Date')['Unit Price'].sum()
        col2.subheader("Sales Trend")
        col2.line_chart(trend)

    st.divider()

    # Monthly sales (again for detailed view)
    if 'Month' in df.columns:
        st.subheader("📅 Monthly Sales Trend")
        monthly_sales = df.groupby('Month')['Unit Price'].sum()
        st.bar_chart(monthly_sales)

# =========================
# 📦 PRODUCTS PAGE
# =========================
elif page == "Products":
    st.title("📦 Product Insights")

    # Product sales chart
    if 'product_name' in df.columns:
        product_sales = df.groupby('product_name')['Unit Price'].sum().sort_values(ascending=False)

        st.subheader("🏆 Top 10 Product Sales")
        st.bar_chart(product_sales.head(10))

        st.divider()

        st.subheader("📊 All Product Sales")
        st.bar_chart(product_sales)

# =========================
# RAW DATA
# =========================
st.divider()
with st.expander("🔍 View Raw Data"):
    st.write(df)