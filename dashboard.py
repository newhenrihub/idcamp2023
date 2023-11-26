import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

customers_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/customers_dataset.csv", delimiter=",")
orders_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/orders_dataset.csv", delimiter=",")
order_items_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/order_items_dataset.csv", delimiter=",")
products_df = pd.read_csv("https://raw.githubusercontent.com/newhenrihub/idcamp2023/main/submission/data/products_dataset.csv", delimiter=",")

products_df.dropna(axis=0, inplace=True)

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

# merge untuk mendapatkan customer dalam data pemesanan
order_customer_df = pd.merge(
    left=orders_df,
    right=customers_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
)

# ambil top 5 state
state_count_df = order_customer_df.groupby(["customer_state"])["customer_state"].count().reset_index(name="count").sort_values("count",ascending=False)
state_count_df.rename(columns={"count":"state_count"},inplace=True)
state_count_df.head(5)

st.header("E-Commerce Dashboard")

col1, col2 = st.columns(2)
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

with col1:
    sns.barplot(y="product_category_name", x="category_count", data=category_count_df.head(5), orient="h", palette=colors, ax=ax)
    ax.set_title("Top 5 product by category", loc="center", fontsize=50)
    ax.set_ylabel("Category Name")
    ax.set_xlabel("Total")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    sns.barplot(y="state_count", x="customer_state", data=state_count_df.head(5), palette=colors, ax=ax)
    ax.set_title("Top 5 most order by state", loc="center", fontsize=50)
    ax.set_ylabel("Total")
    ax.set_xlabel("State Name")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
