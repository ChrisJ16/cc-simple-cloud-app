import streamlit as st
import requests

st.title("Frontend Streamlit, small demonstration app")

backend_url = "https://backendcloudcomputing-a4f4c6cvdcdsghaf.norwayeast-01.azurewebsites.net/api/data"

try:
    response = requests.get(backend_url)
    data = response.json()
    st.success(f"Backend message  : {data['message']}")
except Exception as e:
    st.error(f"The backend couldn't be reached: {e}")
