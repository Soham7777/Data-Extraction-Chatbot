# Data-Extraction-Chatbot

## Overview

This is the repository is for a chatbot service designed to interact with users, provide information, and collect user data in an engaging and informative manner.

The chatbot is powered by the OpenAI GPT-3.5 model and built using FastAPI, Spacy, and Pydantic.

## Installation

Follow these steps to get the API up and running:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/learntube-chatbot-api.git
   ```
2. Create Virutal environment
   ```bash
    conda create --name chatbot-env python=3.11
    conda activate chatbot-env
   ``` 
3. Install the required dependencies using pip:
   ```bash
    pip -q install openai fastapi spacy pydantic
   ```
4. Run the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
   ```

## Work in progress

- [ ] Please note that the API is currently in development. There may be issues with the Spacy model loading "en_core_web_sm",
      particularly if your local machine is having trouble connecting and downloading the model.
      I am trying to resolve this issue to ensure smooth operation of the API.

   

   
    
