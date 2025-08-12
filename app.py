import streamlit as st
import requests
import os

st.set_page_config(page_title="Question Your Documents", layout="wide")
st.title("Question Your Documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader(
    " Upload a PDF or TXT file (Max 2MB)", 
    type=["pdf", "txt"]
)

if uploaded_file:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 2:
        st.error(f" File {uploaded_file.name} is {file_size_mb:.2f}MB. Please upload a file under 2MB.")
    else:
        st.success(f" Uploaded: {uploaded_file.name} ({file_size_mb:.2f} MB)")

        with st.spinner(" Uploading file..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            res = requests.post("http://localhost:8000/upload", files=files)
        
        if res.status_code == 200:
            st.success(" File processed successfully. You can now ask questions.")

            user_input = st.text_input("💬 Ask a question about your document")
            if user_input:
                with st.spinner(" Thinking..."):
                    response = requests.post(
                        "http://localhost:8000/ask",
                        json={"question": user_input}
                    )
                if response.status_code == 200:
                    answer = response.json().get("answer", "⚠ No answer found")
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(" Failed to get a response from the backend.")

