import streamlit as st
from streamlit_gsheets import GSheetsConnection

@st.cache_data
def loadProductPrice():
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    df = conn.read(worksheet="ColorPricing", usecols=list(range(6)), ttl=5)
    df = df.dropna(how="all")

    return df