# -*- coding: utf-8 -*-
"""RAG_QA_Bot

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rrue57xBc0JIb58kpjfLjQRDvjXnTizG
"""

!pip install pinecone-client

!pip install cohere

!pip install transformers datasets

!pip install --upgrade pinecone-client

# Install Pinecone
!pip install pinecone-client

# Install Cohere (if using it)
!pip install cohere

# Install OpenAI (alternative to Cohere, you can pick one)
!pip install openai

# Install Transformers (for working with language models)
!pip install transformers

# Install other helper libraries like datasets
!pip install datasets

import os
from pinecone import Pinecone, ServerlessSpec

# Set up your API key and environment
API_KEY = "df8490a2-ccb3-47f4-8ded-c658d28092df"  # Your Pinecone API key
CLOUD_PROVIDER = "aws"
REGION = "us-east-1"
INDEX_NAME = "multilingual-e5-large"

# Initialize Pinecone using the updated method
pc = Pinecone(
    api_key=API_KEY
)

# Check if the index exists, create it if not
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,  # Example dimension size (adjust if needed)
        metric='euclidean',
        spec=ServerlessSpec(
            cloud=CLOUD_PROVIDER,
            region=REGION
        )
    )

# Connect to the index
index = pc.Index(INDEX_NAME)

print(f"Connected to Pinecone index: {INDEX_NAME}")

from transformers import AutoTokenizer, AutoModel
import torch

# Load a pre-trained embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to convert text to embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Sample data to add to Pinecone
data = [
    {"id": "1", "text": "Pinecone is a vector database used for fast similarity searches."},
    {"id": "2", "text": "Transformers are deep learning models used for NLP tasks."},
    {"id": "3", "text": "Cohere provides natural language processing models as a service."},
]

# Generate embeddings for each document in your data
for item in data:
    item['embedding'] = get_embedding(item['text'])

# Show the data with embeddings
data

# Delete the existing index if it exists
if INDEX_NAME in pc.list_indexes().names():
    pc.delete_index(INDEX_NAME)
    print(f"Deleted existing index: {INDEX_NAME}")

# Create a new index with the correct dimension
pc.create_index(
    name=INDEX_NAME,
    dimension=384,  # Set dimension to match the embedding size
    metric='euclidean',
    spec=ServerlessSpec(
        cloud=CLOUD_PROVIDER,
        region=REGION
    )
)
print(f"Created new index: {INDEX_NAME} with dimension 384")

# Reconnect to the new index
index = pc.Index(INDEX_NAME)
print(f"Connected to Pinecone index: {INDEX_NAME}")

# Sample data to add to Pinecone (same data as before)
data = [
    {"id": "1", "text": "Pinecone is a vector database used for fast similarity searches."},
    {"id": "2", "text": "Transformers are deep learning models used for NLP tasks."},
    {"id": "3", "text": "Cohere provides natural language processing models as a service."},
]

# Generate embeddings for each document in your data
for item in data:
    item['embedding'] = get_embedding(item['text'])

# Insert embeddings into Pinecone
vectors = [(item['id'], item['embedding'].tolist()) for item in data]
index.upsert(vectors)

print("Data has been inserted into Pinecone!")

import numpy as np

# Function to query Pinecone with refined format handling
def query_pinecone(query_text):
    # Convert query text to embedding
    query_embedding = get_embedding(query_text)

    # Ensure the embedding has the correct dimension
    if len(query_embedding) != 384:
        raise ValueError(f"Query embedding has an incorrect dimension: {len(query_embedding)}")

    # Convert embedding to a list of floats
    query_embedding_list = query_embedding.astype(float).tolist()

    # Print the first 10 values of the embedding for verification
    print("Query embedding (first 10 values):", query_embedding_list[:10])

    # Perform the search
    try:
        results = index.query(
            vector=query_embedding_list,
            top_k=3  # Number of top results to retrieve
        )
        return results
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return None

# Example query
query_text = "What is Pinecone used for?"
results = query_pinecone(query_text)

# Print out the results if successful
if results:
    print("Query results:")
    for match in results['matches']:
        print(f"ID: {match['id']}, Score: {match['score']}")
else:
    print("No results returned.")

# Example additional queries
queries = [
    "What is a transformer model?",
    "How does Cohere provide NLP services?",
    "Explain the usage of vector databases."
]

# Perform queries and print results
for query_text in queries:
    results = query_pinecone(query_text)
    print(f"Results for query '{query_text}':")
    if results:
        for match in results['matches']:
            print(f"ID: {match['id']}, Score: {match['score']}")
    else:
        print("No results returned.")
    print()

!pip install cohere



import cohere

# Replace with your actual API key
api_key = 'fLxnpWWyrsYKM1CjH9cFrXRhijqt3CLcn7RF9rog'
cohere_client = cohere.Client(api_key)

try:
    # Test a simple generation request
    response = cohere_client.generate(
        model='command-xlarge-nightly',
        prompt="Test if API key is working.",
        max_tokens=10
    )
    print(response.generations[0].text)
except cohere.error.UnauthorizedError as e:
    print("Authorization error:", e)
except Exception as e:
    print("An error occurred:", e)

import cohere

# Initialize Cohere client with your API key
api_key = 'fLxnpWWyrsYKM1CjH9cFrXRhijqt3CLcn7RF9rog'
cohere_client = cohere.Client(api_key)

try:
    # Make a simple request to generate text
    response = cohere_client.generate(
        model='command-xlarge-nightly',  # Or another model suitable for your use case
        prompt="Test if API key is working.",
        max_tokens=10
    )
    print("Response:", response.generations[0].text)
except cohere.error.UnauthorizedError as e:
    print("Authorization error:", e)
except Exception as e:
    print("An error occurred:", e)

import cohere

# Initialize Cohere client with your API key
api_key = 'fLxnpWWyrsYKM1CjH9cFrXRhijqt3CLcn7RF9rog'
cohere_client = cohere.Client(api_key)

def generate_answer(prompt):
    try:
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # or another model if preferred
            prompt=prompt,
            max_tokens=150  # adjust based on your needs
        )
        return response.generations[0].text
    except cohere.error.UnauthorizedError as e:
        print("Authorization error:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage
query_text = "Explain the usage of vector databases."
answer = generate_answer(query_text)
print("Answer:", answer)

import cohere

# Initialize Cohere client with your API key
api_key = 'fLxnpWWyrsYKM1CjH9cFrXRhijqt3CLcn7RF9rog'
cohere_client = cohere.Client(api_key)

def generate_answer(prompt):
    try:
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # or another model if preferred
            prompt=prompt,
            max_tokens=150  # adjust based on your needs
        )
        return response.generations[0].text
    except cohere.error.UnauthorizedError as e:
        print("Authorization error:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def handle_query(query_text):
    # Generate an answer based on the query
    answer = generate_answer(query_text)
    return answer

# Example usage
query_text = "Explain the usage of vector databases."
answer = handle_query(query_text)
print("Answer:", answer)

# Define a list of test queries
test_queries = [
    "What is the purpose of vector databases?",
    "How do vector embeddings work?",
    "Explain similarity search in vector databases.",
    "What are the applications of vector databases?",
    "How does a vector database differ from a traditional database?"
]

# Test the QA bot with the test queries
for query in test_queries:
    answer = handle_query(query)
    print(f"Query: {query}")
    print(f"Answer: {answer}\n")

# Define a list of test queries
test_queries = [
    "What is the purpose of vector databases?",
    "How do vector embeddings work?",
    "Explain similarity search in vector databases.",
    "What are the applications of vector databases?",
    "How does a vector database differ from a traditional database?"
]

# Test the QA bot with the test queries
for query in test_queries:
    answer = handle_query(query)
    print(f"Query: {query}")
    print(f"Answer: {answer}\n")