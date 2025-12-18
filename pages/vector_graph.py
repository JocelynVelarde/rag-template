import streamlit as st
import backend as rag
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

st.title("Vector Visualization")
st.subheader("View your embeddings in a nice plot that uses PCA")
st.divider()

query = st.text_input("Enter a query to visualize it")

if st.button("Plot"):
    with st.spinner("Calculating from 768 dimensions to 2"):
        # Get data from backend
        data = rag.get_vectors_for_visualization(query)

        # Apply the PCA
        contents = [item["content"] for item in data]
        vectors = [item["vector"] for item in data]
        pca = PCA(n_components=2)
        reduced_vectors = pca.fit_transform(vectors)

        # Create a DataFrame for plotting use px scatter
        df = pd.DataFrame(reduced_vectors, columns=["x", "y"])
        df["content"] = contents
        fig = px.scatter(df, x="x", y="y", hover_data=["content"], title="PCA of Document Vectors")
        st.plotly_chart(fig)
        st.success("Done!")