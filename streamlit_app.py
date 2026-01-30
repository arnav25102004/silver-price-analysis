import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd


st.set_page_config(
    page_title="Silver Price Calculator & Sales Dashboard by ARNAV NARULA",
    layout="wide"
)

st.title(" Silver Price Calculator & Silver Sales Analysis BY ARNAV NARULA 2547115")
st.markdown(
    "This app analyzes silver trend and  it is CIA of Advanced Python MCA A."
)

st.divider()

@st.cache_data
def load_data():
    price_df = pd.read_csv("historical_silver_price.csv")
    sales_df = pd.read_csv("state_wise_silver_purchased_kg.csv")
    return price_df, sales_df

price_df, sales_df = load_data()


st.sidebar.title(" Main Menu")
page = st.sidebar.radio(
    "Select Section",
    ["Silver Price Calculator", "Silver Sales Dashboard"]
)


if page == "Silver Price Calculator":

    st.header("1️ Silver Price Calculator")

    col1, col2, col3 = st.columns(3)

    with col1:
        weight = st.number_input("Enter Weight of Silver", min_value=0.0)
        unit = st.selectbox("Select Unit", ["Grams", "Kilograms"])

    with col2:
        price_per_gram = st.number_input(
            "Current Price per Gram (INR)", min_value=0.0
        )

    with col3:
        currency = st.selectbox("Currency Conversion", ["INR", "USD"])

    if unit == "Kilograms":
        weight = weight * 1000

    total_price_inr = weight * price_per_gram

    if currency == "USD":
        total_price = total_price_inr / 83  
    else:
        total_price = total_price_inr

    st.success(f" Q1 Total Cost of Silver: {total_price:.2f} {currency}")

    st.subheader(" Historical Silver Price Analysis")

    price_filter = st.radio(
        "Filter Silver Prices (INR per kg)",
        ["≤ 20,000", "20,000 – 30,000", "≥ 30,000"]
    )

    if price_filter == "≤ 20,000":
        filtered_df = price_df[price_df["Silver_Price_INR_per_kg"] <= 20000]
    elif price_filter == "20,000 – 30,000":
        filtered_df = price_df[
            (price_df["Silver_Price_INR_per_kg"] > 20000) &
            (price_df["Silver_Price_INR_per_kg"] < 30000)
        ]
    else:
        filtered_df = price_df[price_df["Silver_Price_INR_per_kg"] >= 30000]

    st.line_chart(
        filtered_df.set_index("Month")["Silver_Price_INR_per_kg"]
    )


else:

    st.header("2️ Silver Sales Dashboard")

   
    st.subheader(" State-wise Silver Purchases in India")

   
    india_map = gpd.read_file("Admin2.shp")

    
    state_sales = (
        sales_df
        .groupby("State", as_index=False)["Silver_Purchased_kg"]
        .sum()
    )

  
    merged = india_map.merge(
        state_sales,
        left_on="ST_NM",
        right_on="State",
        how="left"
    )


    fig, ax = plt.subplots(figsize=(10, 10))
    merged.plot(
        column="Silver_Purchased_kg",
        cmap="YlOrRd",
        legend=True,
        edgecolor="black",
        ax=ax
    )

    ax.set_title("State-wise Silver Purchases kg")
    ax.axis("off")
    st.pyplot(fig)

    
    st.subheader(" Top 5 States with Highest Silver Purchases through bar graph")

    top5 = (
        state_sales
        .sort_values("Silver_Purchased_kg", ascending=False)
        .head(5)
    )

    fig2 = px.bar(
        top5,
        x="State",
        y="Silver_Purchased_kg",
        title="Top 5 Silver Purchasing States",
        labels={"Silver_Purchased_kg": "Silver Purchase (kg)"}
    )

    st.plotly_chart(fig2, use_container_width=True)

   
    st.subheader("January Silver Price Trend")

    january_df = price_df[price_df["Month"] == "Jan"].copy()

    
    january_df["Year"] = january_df["Year"].astype(str)

    st.line_chart(
        january_df.set_index("Year")["Silver_Price_INR_per_kg"]
    )

    st.success(" Q2 Silver Sales Dashboard Loaded Successfully")
