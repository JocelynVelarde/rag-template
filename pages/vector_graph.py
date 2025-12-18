import streamlit as st
import backend as rag
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
import numpy as np

st.title("Vector Visualization")
st.subheader("View your embeddings in a nice plot that uses PCA")
st.divider()

query = st.text_input("Enter a query to visualize it")

if st.button("Plot"):
    with st.spinner("Calculating from 768 dimensions to 2"):
        # Get data from backend
        data = rag.get_vectors_for_visualization(query)

        #2. Prepare Data for PCA
        # We need a list of all vectors (Query + Docs)
        all_vectors = [data["query_vector"]] + [d["vector"] for d in data["docs"]]
        all_labels = ["🔴 YOUR QUERY"] + [d["content"][:50] + "..." for d in data["docs"]]
        all_types = ["Query"] + ["Result" for _ in data["docs"]]
        
        # 3. Reduce Dimensions (768 -> 2)
        # We handle the case where we have few points (min 2 for PCA)
        n_components = min(2, len(all_vectors)) 
        pca = PCA(n_components=n_components)
        reduced_vectors = pca.fit_transform(np.array(all_vectors))
        
        # 4. Create DataFrame for Plotly
        df = pd.DataFrame(reduced_vectors, columns=["x", "y"] if n_components == 2 else ["x"])
        if n_components == 1: df["y"] = 0 # Handle 1D case just in case
            
        df["label"] = all_labels
        df["type"] = all_types
        df["full_text"] = ["User Query"] + [d["content"] for d in data["docs"]]

        # 5. Plot Interactive Chart
        fig = px.scatter(
            df, 
            x="x", 
            y="y", 
            color="type",
            text="label",
            hover_data=["full_text"],
            title="Semantic Distance Map",
            size_max=20,
            color_discrete_map={"Query": "red", "Result": "blue"}
        )
        
        # Make it look nice
        fig.update_traces(textposition='top center', marker=dict(size=15))
        fig.update_layout(height=600)
        
        st.plotly_chart(fig, use_container_width=True)
        st.success("Plot generated!")