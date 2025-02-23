from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client for OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY")

# Check if API key exists
if not api_key:
    raise ValueError("Missing OpenRouter API key. Set OPENROUTER_API_KEY in your .env file.")

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key  # Use the API key from the environment
)

# Capture user input
user_input = input("Please enter a word: ")

# Create a chat completion request with strict output instructions
try:
    completion = client.chat.completions.create(
        model="mistralai/mistral-small-24b-instruct-2501:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be given a word. Respond with the color associated with the word. "
                    "Example: sunset=orange, surrender=white, anger=red. "
                    "Respond only with the color name. If no color is associated, reply with 'no color associated with this word'."
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    # Extract the AI response
    response = completion.choices[0].message.content.strip()
    print(response)

except Exception as e:
    print(f"Error: {e}")
