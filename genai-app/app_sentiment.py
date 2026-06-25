import streamlit as st
import pandas as pd 
import os 
import re
import matplotlib.pyplot as plt


# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file (two levels up, then into data/)
    csv_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return csv_path

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text    

# Build the Streamlit UI
st.title("Hello, GenAI!")  # Display a large heading at the top of the page
st.write("This is your GenAI-powered data processing app.")  # Display intro text on the page

# layout side by side
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Ingest Dataset"):
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Dataset loaded!")
        except FileNotFoundError: 
            st.error(f"File Not Found! {csv_path}")

with col2:
    if st.button("📥 Parse Review"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.") 

if "df" in st.session_state:

    st.subheader("Fliter by Product")
    product = st.selectbox(
        "Choose a product",
        ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique())
    )

    st.subheader(f"📁 Reviews for {product}")
    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    if product != "All Products":
        st.bar_chart(grouped.loc[[product]])
    else:
        st.bar_chart(grouped)

    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.hist(filtered_df["SENTIMENT_SCORE"], bins=10, edgecolor='black', alpha=0.7)
    # ax.set_xlabel('Sentiment Score')
    # ax.set_ylabel('Frequency')
    # ax.set_title('Distribution of Sentiment Scores')
    # st.pyplot(fig)