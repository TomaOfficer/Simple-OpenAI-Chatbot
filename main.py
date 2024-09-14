import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

description = """
    You are a highly knowledgeable legal aid assistant specializing in helping users understand their eligibility for legal services and guiding them through various legal procedures. Your role is to provide clear, concise, and accurate legal guidance based on established legal aid criteria, regulations, and policies.
"""

instructions = """
    Respond only to questions related to legal aid services, eligibility, and legal procedures. Do not engage in conversations that fall outside of legal aid, and ensure your responses are always informative, professional, and respectful of legal boundaries. You are not a replacement for a licensed attorney, so always direct users to seek formal legal advice when necessary. When appropriate, provide citations to support your responses.
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
file_paths = ["knowledge/legal-aid-eligibility.md"]
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


# Utilities
def process_citations(message_content):
    citations = []
    if hasattr(message_content, 'annotations'):
        for index, annotation in enumerate(message_content.annotations):
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citation_text = f"[{index + 1}: {cited_file.filename}]"
                message_content.value = message_content.value.replace(
                    annotation.text, citation_text)
                citations.append(f"{citation_text} {cited_file.filename}")
    return message_content.value, citations


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

    # Extract the response from the assistant and process citations
    message_content = messages[0].content[0].text
    assistant_response, citations = process_citations(message_content)

    return jsonify({'response': assistant_response, 'citations': citations})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
