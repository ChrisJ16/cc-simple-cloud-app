import streamlit as st
import requests

st.title("Frontend Streamlit")

backend_url = "https://backendcloudcomputing-a4f4c6cvdcdsghaf.norwayeast-01.azurewebsites.net/api/data"

try:
    response = requests.get(backend_url)
    data = response.json()
    st.success(f"Mesaj de la backend  : {data['message']}")
except Exception as e:
    st.error(f"Nu s-a   putut conecta la backend: {e}")
