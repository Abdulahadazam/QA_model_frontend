import streamlit as st
import requests

st.set_page_config(page_title="Question Your Documents", layout="wide")
st.title("Question Your Documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file (Max 2MB)",
    type=["pdf", "txt"]
)

if uploaded_file:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 2:
        st.error(f"{uploaded_file.name} is {file_size_mb:.2f}MB. Please upload under 2MB.")
    else:
        st.success(f"Uploaded: {uploaded_file.name} ({file_size_mb:.2f} MB)")

    
        with st.spinner("Processing file..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            res = requests.post("http://localhost:8000/upload", files=files)

        if res.status_code == 200:
            data = res.json()
            content = data.get("content", "")
            char_count = len(content)
            st.write(data)
            if char_count < 300:
                st.error("Document is too short to summarize. Please upload a longer document.")
            else:
                with st.spinner("Summarizing document..."):
                    summary_res = requests.post(
                        "http://localhost:8000/summary",
                        json={"content": content}
                    )
                             
                if summary_res.status_code == 200:
                    summary = summary_res.json().get("summary", " No summary available.")
                    st.subheader(" Document Summary")
                    st.write(summary)
                else:
                    st.error("Failed to summarize the document.")
                    summary = None

                st.subheader(" Ask a question about your document")
                user_input = st.text_input("Type your question here")

                if user_input:
                    with st.spinner("Thinking..."):
                        response = requests.post(
                            "http://localhost:8000/ask",
                            json={"question": user_input}
                        )
                    if response.status_code == 200:
                        answer = response.json().get("answer", "⚠ No answer found")
                        st.session_state.messages.append({"role": "user", "content": user_input})
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Failed to get a response from the backend.")

                if st.session_state.messages:
                    st.write("### Chat History")
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            st.markdown(f"**You:** {msg['content']}")
                        else:
                            st.markdown(f"**AI:** {msg['content']}")
        else:
            st.error("Failed to process the uploaded file.")
