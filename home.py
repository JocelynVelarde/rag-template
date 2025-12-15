import streamlit as st
import backend as rag

st.title("Recommendation System with RAG Pipeline")
st.subheader("Add a subheader with more explanation if you want")
st.divider()

# Create a sidebar
# Upload in here the context that goes into MongoDB (knowledge base)
with st.sidebar:
    st.header("Upload context")
    user_text = st.text_area("Enter knowledge here", height=150)

    if st.button("Upload to MongoDB"):
        if user_text:
            with st.spinner("Processisng"):
                rag.ingest_text(user_text)
                st.success("Uploaded")
        else:
            st.warning("Please enter text")

st.header("Ask anything to the chat from our Knowledge Base")

# Initialize the whole message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
prompt = st.chat_input("Ask any question to the chat")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    # Generate rag response in here
    with st.chat_message("ROBOT"):
        with st.spinner("THINKINGSS"):
            response_data = rag.get_rag_response(prompt)
            answer = response_data["answer"]
            sources = response_data["sources"]

            st.markdown(answer)

            # show sources in a expander
            with st.expander("Sources"):
                for i, source in enumerate(sources):
                    st.markdown(f"**Source {i+1}:** {source.page_content}")
            # Append the response to the message history
            st.session_state.message.append({"role": "ROBOT", "content": answer})

