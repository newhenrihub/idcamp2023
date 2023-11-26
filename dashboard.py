import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def create_category_count_df(orders_df,order_items_df,products_df):
    # merge untuk mendapatkan item product yang ada di dalam order
    order_detail_df = pd.merge(
        left=orders_df,
        right=order_items_df,
        how="left",
        left_on="order_id",
        right_on="order_id"
    )
    
    # merge untuk mendapatkan category product dari item yang dipesan
    order_detail_product_df = pd.merge(
        left=order_detail_df,
        right=products_df,
        how="left",
        left_on="product_id",
        right_on="product_id"
    )
    
    # ambil top 5 category
    category_count_df = order_detail_product_df.groupby(["product_category_name"])["product_category_name"].count().reset_index(name="count").sort_values("count",ascending=False)
    category_count_df.rename(columns={"count":"category_count"},inplace=True)
    category_count_df.head(5)
    
    return category_count_df

def create_order_customer_df(orders_df,customers_df):
    # merge untuk mendapatkan customer dalam data pemesanan
    order_customer_df = pd.merge(
        left=orders_df,
        right=customers_df,
        how="left",
        left_on="customer_id",
        right_on="customer_id"
    )
    
    return order_customer_df

def create_state_count_df(order_customer_df):
    # ambil top 5 state
    state_count_df = order_customer_df.groupby(["customer_state"])["customer_state"].count().reset_index(name="count").sort_values("count",ascending=False)
    state_count_df.rename(columns={"count":"state_count"},inplace=True)
    state_count_df.head(5)

    return state_count_df

def create_loyal_cust_count_df(order_customer_df):
    # ambil top 10 loyal customer
    loyal_cust_count_df = order_customer_df.groupby(["customer_unique_id"])["customer_unique_id"].count().reset_index(name="count").sort_values("count",ascending=False)
    loyal_cust_count_df.rename(columns={"count":"loyal_cust_count"},inplace=True)
    loyal_cust_count_df.head(10)

    return loyal_cust_count_df

customers_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/customers_dataset.csv", delimiter=",")
orders_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/orders_dataset.csv", delimiter=",")
order_items_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/order_items_dataset.csv", delimiter=",")
products_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/products_dataset.csv", delimiter=",")

products_df.dropna(axis=0, inplace=True)

category_count_df = create_category_count_df(orders_df,order_items_df,products_df)
order_customer_df = create_order_customer_df(orders_df,customers_df)
state_count_df = create_state_count_df(order_customer_df)
loyal_cust_count_df = create_loyal_cust_count_df(order_customer_df)

st.header("E-Commerce Dashboard")

col1, col2 = st.columns(2)
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

with col1:
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.barplot(y="product_category_name", x="category_count", data=category_count_df.head(5), orient="h", palette=colors, ax=ax)
    ax.set_title("Top 5 orders by product category", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.barplot(y="state_count", x="customer_state", data=state_count_df.head(5), palette=colors, ax=ax)
    ax.set_title("Top 5 orders by state", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 20))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(y="customer_unique_id", x="loyal_cust_count", data=loyal_cust_count_df.head(10), palette=colors, ax=ax)
ax.set_title("Top 10 loyal customers", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
