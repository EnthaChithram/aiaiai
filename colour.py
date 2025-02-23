import openai
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client using API key from .env
client = openai.OpenAI()

# Define model and assistant/thread IDs
model = "gpt-3.5-turbo"
assistant_id = "asst_AC3FMMkVf4R4IieoDzs8aIZJ"
thread_id = "thread_RCm5UiovBczDZakZEaJGKwol"

# Send a message
message_content = "the color of paper"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message_content
)

# Start the assistant run
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Hero"
)

# 🔄 Wait for the run to complete

while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    print(f"Run Status: {run.status}")
    print(f"Run Error: {run.last_error}")

    print(f"Run Status: {run.status}")  # Debugging line
    if run.status in ["completed", "failed", "cancelled"]:
        break
    time.sleep(2)  # Wait before checking again


# Retrieve and print messages
messages = client.beta.threads.messages.list(thread_id=thread_id)
if messages.data:
    last_message = messages.data[0]
    response = last_message.content[0].text.value
    print("Response:", response)

# Retrieve and print run steps
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print("Run Steps:", run_steps.data)




# def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
#     """

#     Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
#     :param thread_id: The ID of the thread.
#     :param run_id: The ID of the run.
#     :param sleep_interval: Time in seconds to wait between checks.
#     """
#     while True:
#         try:
#             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#             if run.completed_at:
#                 elapsed_time = run.completed_at - run.created_at
#                 formatted_elapsed_time = time.strftime(
#                     "%H:%M:%S", time.gmtime(elapsed_time)
#                 )
#                 print(f"Run completed in {formatted_elapsed_time}")
#                 logging.info(f"Run completed in {formatted_elapsed_time}")
#                 # Get messages here once Run is completed!
#                 messages = client.beta.threads.messages.list(thread_id=thread_id)
#                 last_message = messages.data[0]
#                 response = last_message.content[0].text.value
#                 print(f"Assistant Response: {response}")
#                 break
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the run: {e}")
#             break
#         logging.info("Waiting for run to complete...")
#         time.sleep(sleep_interval)


# # === Run ===
# wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# # ==== Steps --- Logs ==
# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Steps---> {run_steps.data[0]}")