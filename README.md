Interactive QA Bot Interface
This project implements an interactive QA bot interface that allows users to upload PDF documents and ask questions based on the content of the uploaded document. The backend uses Pinecone for indexing and querying, and Cohere for generating embeddings. The frontend is built using Gradio.

Live Demo
You can view the live demo of the QA bot interface here: Gradio Live Demo

Prerequisites
Before running the project, make sure you have the following:

Python (preferably Python 3.7 or newer)
Pinecone API Key: Get your Pinecone API Key
Cohere API Key: Get your Cohere API Key
Setup Instructions
Clone the Repository

bash
Create a Virtual Environment (optional but recommended)

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Required Packages

Install the necessary Python packages using pip. Since you’re using Google Colab, you might need to install them directly in the Colab environment:

python
Copy code
!pip install gradio pinecone-client cohere
Set Up Environment Variables

Create a .env file in the root directory of your project with the following content:

text
Copy code
PINECONE_API_KEY=your_pinecone_api_key
COHERE_API_KEY=your_cohere_api_key
Replace your_pinecone_api_key and your_cohere_api_key with your actual API keys.

Run the Application

Run the Gradio app using the following command:

bash
Copy code
python app.py
The application should now be running on http://localhost:7860. If you have deployed it on a cloud service, use the provided URL to access it.

Usage Instructions
Upload a PDF Document

Click on the "Upload PDF" button and select the PDF document you want to use.

Ask a Question

Enter your question related to the content of the uploaded PDF in the "Ask a Question" textbox.

View the Response

The system will process your query and return an answer based on the content of the uploaded document. You will also see the relevant document segments alongside the answer.

Troubleshooting
If the Gradio interface does not load:

Check that you have activated the virtual environment and installed all necessary packages.
Ensure your API keys are correct and have the necessary permissions.
Verify that Pinecone and Cohere services are up and running.
If you encounter errors related to Pinecone or Cohere:

Double-check your API keys and ensure they are correctly set in the .env file.
Make sure you have the right API key permissions and the index exists.
Contributing
Feel free to fork the repository and submit pull requests with improvements or bug fixes. For major changes, please open an issue to discuss what you would like to change.

License
This project is licensed under the MIT License - see the LICENSE file for details.
