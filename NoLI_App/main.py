import streamlit as st

st.title("NoLI™ Connection Test")

if st.button("Click Me"):
    st.toast("Hello World!")
    st.success("The Logic Engine is Online.")