import streamlit as st
import requests

st.title("Question Your Documents")

uploaded_files = st.file_uploader("Select a file", accept_multiple_files=True, type=["pdf", "txt", "csv"])

if uploaded_files is not None:
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.size > 2 * 1024 * 1024:
            st.error(f"File {uploaded_file.name} size exceeds the limit. Please upload a file smaller than 2MB")
            uploaded_file = None
        else:
            st.success(f"File {uploaded_file.name} uploaded successfully")
            file_contents = uploaded_file.read()
            # st.write(file_contents)

           
                