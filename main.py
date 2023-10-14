from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import openai
import re
import uvicorn

openai.api_key = ""

# Initialize global variables to store extracted information
global_info = {
    "name": "",
    "email": "",
    "address": "",
    "education": "",
    "phone": "",
    "dob": "",
}

#Function to extract information from the user 
#Function to extract information from the user 
def extract_information(text):
    global global_info

    # Load the English NLP model in spaCy
    nlp = spacy.load("en_core_web_sm")

    # Process the text with spaCy
    doc = nlp(text)

    # Extract information using spaCy's NER
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            global_info["name"] = ent.text
        elif ent.label_ == "GPE":
            global_info["address"] = ent.text
        elif ent.label_ == "DATE":
            # Check if the date is in a valid format (e.g., YYYY-MM-DD)
            if re.match(r'\d{4}-\d{2}-\d{2}', ent.text):
                global_info["dob"] = ent.text

    # Extract education information using regular expressions
    education_keywords = r"(secondary school|high school|diploma|bachelor's|bachelors|master's|masters)"
    education_match = re.search(education_keywords, text, re.IGNORECASE)

    if education_match:
        global_info["education"] = education_match.group(0)

    # Access phone number and email using regular expressions
    phone_pattern = r'\d{10,14}' #check for digits 0-9 within range of 10-14 numbers
    email_pattern = r'\S+@\S+' #pattern matching for email

    phone_match = re.search(phone_pattern, text)
    email_match = re.search(email_pattern, text)

    if phone_match:
        global_info["phone"] = phone_match.group()
    if email_match:
        global_info["email"] = email_match.group()



#initialize message history with business object and first prompt
messages=[
      {"role": "system", "content": """
                        You are Jarvis, the AI chatbot, represents Learntube, specializing in online education. 
                        Your primary task is data collection during from user with engaging conversations about AI and the companys objective, avoiding the feel of a static Google form. 
                        You're to gather essential info_item = (name, email, address, phone, DOB, and education). Here are some Key Actions you need to follow strictly.
                        Key Actions:
                        !!Important : (1. Ask for each element from info_item in between 2-3 user and assistant conversations.Begin with requesting the user's name and subsequently  
                        collect all the elements within info_item similarly like each element in between 2-3 user and assistant conversations before the user exits the conversation)
                        2. Request each detail with context and explanations. For example, ask for the email for newsletters, 
                         date of birth (DOB) for age-oriented courses, and education level for expertise-related courses. 
                        3. Keep conversations AI-centric, steering back to the company's objectives and AI topics.)
                        4. Strictly Maintain  your responses less than 100 words 
                        5. Reassure users about data privacy and request explicit consent for storage and use.
                        6. Validate name (min. 2 characters), email with valid domains (.com, .org, .net).
                        7. Ensure proper addresses, excluding unrealistic inputs.
                        8. Check DOB format (YYYY-MM-DD) and realism. 
                        9. Verify phone numbers (under 14 digits) with recognized formats.
                        10. Prompt for valid education levels (e.g., secondary school, bachelors).
                        11. Provide guidance and assistance for incorrect or incomplete responses.
                        12. Offer help to struggling users.
                        13. Prompt for accurate details if gibberish or irrelevant info is given.
                        14. Prioritize ethical considerations and avoid harmful content.
                        15. Convince users that providing info enhances their experience.
                        16. Avoid overwhelming users with excessive information.
                        17. Omit instructions when users provide info correctly.
                        Keep all this in mind during your conversations.
"""},
      {"role": "assistant", "content": "Hey There! Tech Explorer , How may I help you today?"}
  ]

# Funtion to store message history
def update_messages(messages, role, content):
  messages.append({"role": role, "content": content})
  return messages

#instance of the gpt model to give response for user request.
def chatgpt_response(messages):
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,
  temperature=0.1
  )
  return  response['choices'][0]['message']['content']

# Function to handle user messages
def handle_user_message(user_input):
    extract_information(user_input)
    messages.append({"role": "user", "content": user_input})
    model_response = chatgpt_response(messages)
    messages.append({"role": "assistant", "content": model_response})
    return model_response

# Initialize the FAST API app
app = FastAPI()

# Define data model for request and response
class UserMessage(BaseModel):
    content: str

class BotResponse(BaseModel):
    content: str

@app.get("/")
def home():
    return {"health_check": "OK"}

# Route to handle user messages
@app.post("/message", response_model=BotResponse)
def handle_message(user_message: UserMessage):
    user_input = user_message.content
    model_response = handle_user_message(user_input)
    return {'content': model_response}

# Your chatgpt_response function here

# Run the FAST API app
if __name__ == "__main__":
    
    uvicorn.run(app,host='127.0.0.1',port = 8000)

    #Run with this command: uvicorn main:app --reload