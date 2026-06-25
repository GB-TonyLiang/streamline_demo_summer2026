import ollama 
import streamlit as st

@st.cache_data
def get_response(prompt, temperature):
    # response = client.responses.create(
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
            ],
        options={
            "temperature":temperature,
            "num_predict":100
        }
    )
    return response['message']['content']



# st.title("GPT-4o-mini Chatbot")
st.title("Llama 3.2 Chatbot")

user_prompt = st.text_input(
    "Enter your prompt:", 
    "What is the capital of France?"
    )

temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01,
)

with st.spinner("Thinking..."):
    response = get_response(user_prompt, temperature)
    st.write(response)
