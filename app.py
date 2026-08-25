import pandas as pd
import streamlit as st

from services.order_assistant import answer_order_question
from services.reply_assistant import generate_customer_reply
from services.seller_insights import generate_seller_insights

st.set_page_config(page_title="SellAssist AI", page_icon="🛍️", layout="wide")

# Data
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
orders_with_products = orders.merge(
    products[["product_id", "name"]], on="product_id", how="left"
)

# Title
st.title("SellAssist AI")
st.caption("Asisten bisnis AI untuk penjual e-commerce")

# Dashboard Utama
total_orders = len(orders)
completed_orders = orders[orders["status"] == "Selesai"]
total_revenue = completed_orders["total"].sum()
pending_orders = len(orders[orders["status"] == "Menunggu Pembayaran"])
low_stock = len(products[products["stock"] <= 5])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pesanan", total_orders)
col2.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
col3.metric("Pesanan Menunggu Pembayaran", pending_orders)
col4.metric("Produk Perlu Restock", low_stock)

st.divider()

# -------------------------------
# Inventaris
# -------------------------------
st.subheader("Inventaris")

low_stock_products = products[products["stock"] <= 5]

if len(low_stock_products) > 0:
    st.warning("Ada beberapa produk yang perlu di-restock.")

st.dataframe(
    products,
    width="stretch",
    hide_index=True,
    column_config={
        "product_id": "ID Produk",
        "name": "Nama",
        "price": "Harga (Rp)",
        "stock": "Jumlah Stok",
        "category": "Kategori",
    },
)

# -------------------------------
# Pesanan
# -------------------------------
st.subheader("Pesanan")

st.dataframe(
    orders_with_products[["order_id", "name", "quantity", "status", "total"]].rename(
        columns={
            "order_id": "ID Order",
            "name": "Nama",
            "quantity": "Jumlah Stok",
            "status": "Status",
            "total": "Total Harga (Rp)",
        }
    ),
    width="stretch",
    height="content",
    hide_index=True,
)

# -------------------------------
# Asisten Chat Pelanggan
# -------------------------------
st.divider()

st.subheader("Asisten Chat Pelanggan")
st.caption("Buat balasan cepat dan ramah untuk chat pelanggan.")

customer_message = st.text_area(
    "Chat Pelanggan", placeholder="Contoh: Halo kak, ini barangnya masih ada?"
)

product_names = products["name"].tolist()

selected_product = st.selectbox("Pilih Produk", product_names)

selected_product_data = products[products["name"] == selected_product].iloc[0]

product_info = f"""
Nama Produk: {selected_product_data["name"]}
Harga: Rp {selected_product_data["price"]:,.0f}
Stok: {selected_product_data["stock"]}
"""

tone = st.selectbox("Mode Balasan", ["Ramah", "Profesional", "Santai"])

if st.button("Buat Chat Balasan"):
    if not customer_message:
        st.warning("Silahkan masukkan chat pelanggan terlebih dahulu.")
    else:
        with st.spinner("Sedang menyusun balasan..."):
            reply = generate_customer_reply(customer_message, product_info, tone)

        st.write("**Rekomendasi Chat Balasan:**")
        st.code(reply, language=None)

# -------------------------------
# Asisten Pesanan
# -------------------------------
st.divider()

st.subheader("Asisten Pesanan")
st.caption("Ajukan pertanyan seputar data pesanan dan penjualan Anda.")

order_question = st.text_input(
    "Tanya SellAssist tentang pesanan Anda",
    placeholder="Contoh: Berapa banyak pesanan yang berstatus sedang menunggu pembayaran?",
)

order_data = (
    orders_with_products[["order_id", "name", "quantity", "status", "total"]]
    .rename(columns={"name": "produk"})
    .to_string(index=False)
)

inventory_data = (
    products[["product_id", "name", "price", "stock", "category"]]
    .rename(
        columns={
            "name": "produk",
            "price": "harga",
            "stock": "stok",
            "category": "kategori",
        }
    )
    .to_string(index=False)
)

context = f"""
### DATA PESANAN:
{order_data}

### DATA INVENTARIS:
{inventory_data}
"""

if st.button("Tanya SellAssist AI"):
    if not order_question:
        st.warning("Silahkan masukkan pertanyaan Anda.")
    else:
        with st.spinner("Sedang menganalisis data..."):
            answer = answer_order_question(order_question, context)

        st.write("**Jawaban SellAssist:**")
        st.info(answer)

# -------------------------------
# Insight Penjualan
# -------------------------------
st.divider()

st.subheader("Insight Penjualan")
st.caption("Dapatkan analisis dan rekomendasi otomatis untuk bisnis Anda.")

if st.button("Analisis Toko Saya"):
    with st.spinner("Sedang menganalisis toko Anda..."):
        insights = generate_seller_insights(inventory_data, order_data)

    st.write("**Hasil Analisis Toko:**")
    st.markdown(insights)
