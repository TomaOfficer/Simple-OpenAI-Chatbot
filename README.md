# Simple OpenAI Chat
This repository serves as a template for building an AI-powered Retrieval-Augmented Generation (RAG) chatbot using OpenAI's Assistant API with the file search tool. The goal of this project is to enable anyone to experience the capabilities of a RAG-based app, and to invite legal professionals to consider how they might leverage this technology to create powerful, knowledge-driven applications.

Table of Contents: 
- Introduction
- Getting Started
  - Prerequisites
  - Project Structure
- Configuration
  - Setting Up the OpenAI API Key
  - Customizing the Knowledge Base
- Running the Application
- Deploying the Application
- Troubleshooting

## Introduction
This project template provides a ready-to-use framework for building an AI chatbot that integrates with your own custom knowledge base. It uses OpenAI's Assistant API and the file search tool to deliver responses grounded in the documents you provide, making it an ideal starting point for legal professionals or anyone looking to build a specialized AI assistant.

### Why Build This?
The template is designed to show how combining a powerful language model with document retrieval (RAG) can enhance the accuracy and relevance of responses. See firsthand how a RAG-based system works and experiment with building your own.

## Getting Started
### Prerequisites
Before setting up the application, ensure you have the following:

1. A Replit account: You can sign up for free at replit.com
2. An OpenAI API key: You can get one from OpenAI's API key page.
3. A knowledge base file: The chatbot leverages a Markdown file to inform its responses. You will replace the existing example with your own file.

### Project Structure
The project is organized into several key directories and files:

`knowledge/`: This directory contains your knowledge base files in Markdown format. These files are used by the chatbot to provide informed responses based on their content. Replace the provided legal-aid-eligibility.md file with your own Markdown file(s) as needed.

`public/`: Contains static assets like CSS stylesheets for styling the front-end of your application. The included style.css can be modified to customize the appearance of your app.

`templates/`: Holds HTML templates that define the structure of your web pages. The main template is index.html, which renders the primary interface for interacting with the chatbot.

`main.py`: The core application file, written in Python using Flask. This file handles API requests, integrates with the OpenAI Assistant, and serves the web application. It also includes configuration for setting up the assistant and linking it with your knowledge base.

## Configuration
### Setting Up the OpenAI API Key
Sign up or log in to OpenAI and navigate to the API keys section.
Click Create new secret key and copy the generated key.
In Replit, click on the Secrets tab in the left-hand sidebar.
Add a new secret:
Key: OPENAI_API_KEY
Value: Paste your OpenAI API key here.
Click Save to securely store the key in Replit. This key will now be accessible to your application.

### Customizing the Knowledge Base
To make the chatbot relevant to your domain, replace the sample knowledge base file with your own:

Navigate to the knowledge/ directory in your Replit project.
Replace the legal-aid-eligibility.md file with a new Markdown file that contains the content you want your assistant to use.
If you use a different filename or add multiple files, update the file path references in main.py to include these new files.

## Running the Application
Click the green Run button at the top of the Replit editor.
The Flask server will start and display a URL in the Replit console (e.g., https://your-repl-name.repl.co).
Open the URL to access your AI chatbot in a new tab.
You can now interact with the chatbot by asking questions related to your knowledge base.
Note: On the first run, the application might take longer to start as it installs dependencies and initializes with your knowledge base. Subsequent runs will be faster.

## Deploying the Application
Although Replit allows free deployment of static sites, this chatbot is a dynamic web application built with Flask and requires a server to run, which cannot be hosted as a static site. However, students can still share and run their chatbot on Replit for free:

1. Run the Chatbot on Replit
After configuring your app, click the green Run button at the top of the Replit editor. Once the server starts, Replit will provide a URL (e.g., https://your-repl-name.repl.co) in the Replit console.

2. Share the App
You can share this URL with anyone, and they will be able to interact with your chatbot as long as the Repl is active.

3. Deploy the App
To make your app permanently accessible, you can deploy it on Replit. Here’s how:
- Click the Deploy button in the Replit editor.
- When prompted to enter a Run Command, type: run
This command uses the configuration specified in your .replit file to start the Flask server (python3 main.py). Complete the deployment process, and Replit will provide you with a permanent URL.

4. Keep the App Running
If you want your app to stay active without manually starting it each time, you'll need to upgrade to Replit’s Hacker or Pro plan, which includes the Always On feature. This option ensures your server remains running 24/7.

While deploying to Replit's static site hosting is not possible for this dynamic chatbot, students can still experience the full functionality of the chatbot by running it directly within the Replit environment, sharing the active link, or deploying it with the correct run command.

## Troubleshooting
Missing API Key: If the app returns an error related to the OpenAI API key, double-check that you have added the key to the Secrets tab and that it matches the variable name OPENAI_API_KEY.

Long Load Times: The first run can be slow due to dependency installation and file indexing. If it takes too long, try stopping and re-running the app.

Knowledge Base Not Recognized: Ensure your Markdown file is correctly formatted and the path is properly referenced in main.py.