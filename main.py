import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

description = """
    You are a chatbot for the Thomas Officer design studio who responds to prospective clients with a precise response regarding Thomas' policies.
"""

instructions = """
    Do not engage in any other conversations that isn't related to Thomas' services.
"""

assistant = client.beta.assistants.create(
    name="Professional Assistant",
    description=description,
    instructions=instructions,
    model="gpt-4o",
    tools=[{
        "type": "file_search"
    }],
)

# For debugging
print(f"Assistant created with ID: {assistant.id}")

# Create vector store
vector_store = client.beta.vector_stores.create(name="Policies")
print(f"Vector store ID - {vector_store.id}")

# Upload Policy File into Vector Store
file_paths = ["knowledge/policy.md"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)

# Update assistant with new vector store
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {
        "vector_store_ids": [vector_store.id]
    }},
)

# Create Flask app
app = Flask('app')


# Routes
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Create a thread
    thread = client.beta.threads.create(messages=[{
        "role": "user",
        "content": user_message,
    }])

    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.
    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,
                                                   assistant_id=assistant.id)

    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    # Extract the response from the assistant
    assistant_response = messages[0].content[0].text.value

    return jsonify({'response': assistant_response})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

# message_content = messages[0].content[0].text
# annotations = message_content.annotations
# citations = []
# for index, annotation in enumerate(annotations):
#     message_content.value = message_content.value.replace(
#         annotation.text, f"[{index}]")
#     if file_citation := getattr(annotation, "file_citation", None):
#         cited_file = client.files.retrieve(file_citation.file_id)
#         citations.append(f"[{index}] {cited_file.filename}")

# print(message_content.value)
# print("\n".join(citations))
