import streamlit as st
from load_data import loadProductPrice

df_product_price = loadProductPrice()

list_product = (
    df_product_price["Nama Produk"]
    .dropna()
    .unique()
    .tolist()
)

if "chemical_items" not in st.session_state:
    st.session_state.chemical_items = []

with st.container(border=True):
    st.markdown("### Input Produk Chemical")

    selected_produk = st.selectbox(
        "Nama Produk",
        list_product
    )

    gramasi = st.number_input(
        "Gramasi Digunakan (gr)",
        min_value=0.0,
        step=1.0
    )

    col_add, col_reset = st.columns(2)

    if col_add.button("➕ Tambah", use_container_width=True):
        harga_jual = (
            df_product_price.loc[
                df_product_price["Nama Produk"] == selected_produk,
                "Harga Jual/Gram"
            ]
            .iloc[0]
        )

        st.session_state.chemical_items.append({
            "Nama Produk": selected_produk,
            "Gramasi": gramasi,
            "Harga / Gram": harga_jual,
            "Subtotal": harga_jual * gramasi
        })

    if col_reset.button("🔄 Reset", use_container_width=True):
        st.session_state.chemical_items = []
        st.rerun()


st.markdown("### Produk Digunakan")

if st.session_state.chemical_items:
    for idx, item in enumerate(st.session_state.chemical_items):
        with st.container(border=True):
            st.write(f"**{item['Nama Produk']}**")
            st.write(f"Gramasi : {item['Gramasi']} gr")
            st.write(f"Harga   : Rp {item['Harga / Gram']:,.0f} / gr")
            st.write(f"Subtotal: **Rp {item['Subtotal']:,.0f}**")

            if st.button("❌ Hapus", key=f"delete_{idx}", use_container_width=True):
                st.session_state.chemical_items.pop(idx)
                st.rerun()
else:
    st.info("Belum ada produk yang ditambahkan.")

total_cost = sum(
    item["Subtotal"] for item in st.session_state.chemical_items
)

st.divider()
st.metric(
    "Total Estimasi Cost Chemical",
    f"Rp {total_cost:,.0f}"
)
