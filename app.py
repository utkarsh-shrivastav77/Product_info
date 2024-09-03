import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_claude_response(prompt):
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_summary_pros_cons(product, info):
    prompt = f"""Given the following product and information:

Product: {product}
Information: {info}

Please provide:
1. A short summary of the product (2-3 sentences)
2. A list of pros (advantages)
3. A list of cons (disadvantages)

Format the response with clear headings for Summary, Pros, and Cons. Use bullet points for pros and cons."""
    return get_claude_response(prompt)

st.title("Product Summary, Pros and Cons Generator")

product_name = st.text_input("Enter the name of the product:")
product_info = st.text_area("Enter additional information about the product:", height=100)

if st.button("Generate Summary, Pros and Cons"):
    if product_name and product_info:
        with st.spinner("Generating summary, pros and cons..."):
            result = generate_summary_pros_cons(product_name, product_info)
            st.markdown(result)
    else:
        st.warning("Please enter both the product name and information.")

st.sidebar.header("About")
st.sidebar.info(
    "This app uses Claude AI to generate a summary, pros, and cons for a given product. "
    "Enter a product name and additional information, then click the button to get a comprehensive overview."
)
