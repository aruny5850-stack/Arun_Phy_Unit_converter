import streamlit as st

st.title("My First Streamlit App")

st.write("Hello! My Python app is working.")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.success(f"Hello {name}!")
