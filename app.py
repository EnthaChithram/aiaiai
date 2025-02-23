from flask import Flask, render_template, request, jsonify  # Import jsonify for sending JSON responses
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS
import logging


# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENROUTER_API_KEY")

# Check if API key exists
if not api_key:
    logging.error("⚠️ OPENROUTER_API_KEY is NOT set!")
else:
    logging.debug(f"✅ OPENROUTER_API_KEY is set: {api_key[:5]}*****")

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key  # Use the API key from the environment
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Allow requests from your frontend

@app.route('/', methods=['GET', 'POST'])
def index():
    color_output = ""
    if request.method == 'POST':
        data = request.get_json()  # Parse the incoming JSON data
        user_input = data['word']  # Get user input from the JSON body
        completion = client.chat.completions.create(
            
            model="mistralai/mistral-small-24b-instruct-2501:free",
            messages=[
                {
                    "role": "system",
                    "content": "only think for 10 seconds. you will be given a word as an input. your output should be the color associated with the word. example: sunset=orange. another example:surrender=white. another example:anger=red. your output should always be a color. only a color. Make sure to respond with the color only. If there are multiple colors associated with the word, you should respond with the most logical color. If there is no color associated with the word, you should respond with 'no color associated with this word'."
                },
                {
                    "role": "user",
                    "content": user_input  # Use the captured user input
                }
            ]
        )
        color_output = completion.choices[0].message.content.strip()  # Get the output color

        response = jsonify({"color": color_output})  # Return the color as a JSON response
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all origins
        return response


    # return render_template('index.html', color=color_output)
    return jsonify({"color": color_output})  # Return only the color as a JSON response

@app.route('/check', methods=['GET'])
def check():
    return "connected"


if __name__ == '__main__':
    app.run(debug=True)
