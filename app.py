from flask import Flask, request, jsonify
import anthropic
import os
from dotenv import load_dotenv

app = Flask(__name__)

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

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    product_name = data.get('product_name')
    product_info = data.get('product_info')

    if not product_name or not product_info:
        return jsonify({"error": "Please provide both product name and product information."}), 400

    result = generate_summary_pros_cons(product_name, product_info)
    return jsonify({"result": result})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)

