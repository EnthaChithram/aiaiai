from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Capture user input
user_input = input("Please enter a word: ")

# Create a chat completion request with strict output instructions
completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Replace with your site URL if needed.
        "X-Title": "<YOUR_SITE_NAME>",      # Optional. Replace with your site name if needed.
    },
    model="mistralai/mistral-small-24b-instruct-2501:free",
    messages=[
        {
            "role": "system",
            "content": "only think for 10 seconds. you will be given a word as an input. your output should be the color associated with the word. example: sunset=orange. another example:surrender=white. another example:anger=red. your output should always be a color. only a color. Make sure to respond with the color only. If there are multiple colors associated with the word, you should respond with the first color in the list. If there is no color associated with the word, you should respond with 'no color associated with this word'."
        },
        {
            "role": "user",
            "content": user_input  # Use the captured user input
        }
    ]
)

# Print the last word of the message content
last_word = completion.choices[0].message.content.strip().split()[-1]

print(completion.choices[0].message.content)
