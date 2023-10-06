#importing necessary libraries 
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_tagging_chain_pydantic,LLMChain
import pandas as pd
from pydantic import BaseModel, Field
import streamlit as st
import time

__version__ = "GPT3"

#set the openai environment

os.environ["OPENAI_API_KEY"] = ""


# Information to extract : Name, email, phone no, Address, Date of birth, Education.

# Defining the schema for above use case with Pydantic

# make sure this is set None else it will thow error if we define it as compulsory field with ' ... '

class Tags(BaseModel):

    Name: str = Field( 
        None,  
        
        description="This will contain information on full name of the user")
    
    Email: str = Field(
        None,
        description="This will contain information on email of the user")
    
    Phone : int = Field(
        None, 
        description="This will contain information on phone number of the user")
    
    Address : str = Field(
        None, 
        description="This will contain information on Address of the user")
    
    DOB: str = Field(
        None, 
        description="This will contain information on Date of Birth of the user")

    Education: str = Field(
       None, 
        description="This will contain information on Level Of Education of the user") 
    
#Define the model

llm = ChatOpenAI(temperature=0)
# chain = create_tagging_chain_pydantic(Tags, llm)

#This function will check for fields which are still yet to be filled with information required
def check_empty_fields(any_user_details):
    ask_for = [field for field, value in any_user_details.__dict__.items() if value in [None, "", 0]]
    
    return ask_for

#Validating the response and adding it to the current instance of Object
def fill_details(current_details: Tags, new_details: Tags):

    non_empty_details = {k: v for k, v in new_details.__dict__.items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details 

#this function will provide a template to agent on how to proceed with the conversation

def ask_for_info(ask_for):

  # prompt template 1
  first_prompt = ChatPromptTemplate.from_template(
      "Below is are some things to ask the user for in a coversation way. you should only ask one question at a time even not all at once \
      don't ask as a list! Don't greet the user ! . Strict rule: Only if user is hesitant to response or not giving information tell convince them their data is safe . If the ask_for list is empty then thank them and and tell well get back soon \n\n \
      ### ask_for list: {ask_for}"
  )


  # info_gathering_chain
  info_gathering_chain = LLMChain(llm=llm, prompt=first_prompt)
  ai_chat = info_gathering_chain.run(ask_for=ask_for)
  return ai_chat

#This function will help to keep a track of variable we are storing and making sure not to repeat any information

def filter_response(text_input, user_details):
    chain = create_tagging_chain_pydantic(Tags, llm)
    res = chain.run(text_input)
    # add filtered info to the
    user_details = fill_details(user_details,res)
    ask_for = check_empty_fields(user_details)
    return user_details, ask_for

# function to store data in csv which will take user details as input 

def append_data_to_csv(new_data_dict):
    # Define the column names
    columns = ['Name', 'Email', 'Phone', 'Address', 'DOB', 'Education']

    # Check if the CSV file exists or create a new one
    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)

    # Append the new data as a row to the DataFrame
    df = df.append(new_data_dict, ignore_index=True)

    # Save the DataFrame to the CSV file
    df.to_csv('data.csv', index=False)


#Initialing empty user 

test_user_details = Tags(Name="",
                        Email	="",
                        Phone= 0,
                        Address="",
                        DOB="",
                        Education="")



#Starting with chat bot interface using stream lit 

#Setting the heading for the chatbot 

st.title("Unlock Excellence : Elevate Your Skills with Top Learning Content, Certifications, and Career Support! Share Your Info Below for Personalized Guidance on Your Journey to Success.")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# #Initial Conversation
# message = ask_for_info()
# st.chat_message("Assitant").markdown(message)

# user_text = st.chat_input("Give your response here")
# st.chat_message("User").markdown(user_text)

# user_details, ask_for = filter_response(user_text, test_user_details)



# ask_for = True
# run_once_flag = True


#Initial Message

message = ask_for_info(['Name'])

st.write(f'Assitant : {message}')

user_input = st.text_input('You can respond here',key = 'val1' )
st.write(f'User: {user_input}')

user_details, ask_for = filter_response(user_input, test_user_details)

time.sleep(55)

# check on ask condition 

if ask_for:

    message = ask_for_info(ask_for)
    st.write(f'Assitant : {message}')

    user_input = st.text_input('You can respond here',key = 'val2' )
    st.write(f'User: {user_input}')

    user_details, ask_for = filter_response(user_input, test_user_details)
    pass

time.sleep(55)

if ask_for:

    message = ask_for_info(ask_for)
    st.write(f'Assitant : {message}')

    user_input = st.text_input('You can respond here',key = 'val3' )
    st.write(f'User: {user_input}')

    user_details, ask_for = filter_response(user_input, test_user_details)

time.sleep(55)

if ask_for:

    message = ask_for_info(ask_for)
    st.write(f'Assitant : {message}')

    user_input = st.text_input('You can respond here',key = 'val4' )
    st.write(f'User: {user_input}')

    user_details, ask_for = filter_response(user_input, test_user_details)

time.sleep(55)

if ask_for:

    message = ask_for_info(ask_for)
    st.write(f'Assitant : {message}')

    user_input = st.text_input('You can respond here',key = 'val5' )
    st.write(f'User: {user_input}')

    user_details, ask_for = filter_response(user_input, test_user_details) 

time.sleep(55)    

if ask_for:

    message = ask_for_info(ask_for)
    st.write(f'Assitant : {message}')

    user_input = st.text_input('You can respond here',key = 'val6' )
    st.write(f'User: {user_input}')

    user_details, ask_for = filter_response(user_input, test_user_details)   



# st.write(f'User : {user_input}')

#     user_input = st.chat_input("Enter your response",key = f'{i}')
#     st.chat_message("user").markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     time.sleep(30)

#     user_details, ask_for = filter_response(user_input, test_user_details)

#     time.sleep(30)




# #Rest of the conversation
# while ask_for:

#     if run_once_flag:
    
#         #Initial Conversation
        
#         message = ask_for_info()
        
#         # Display user message in chat message container
#         st.chat_message("Assitant").markdown(message)
#         st.session_state.messages.append({"role": "assistant", "content": message})

#         user_input = st.chat_input("Enter your first response")

#         # Display user message in chat message container
#         st.chat_message("user").markdown(user_input)

#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         user_details, ask_for = filter_response(user_input, test_user_details)

#         # Set the flag to False after running the code
#         run_once_flag = False
#         time.sleep(30)

# #for the rest of the questions 
#     ai_response = ask_for_info(ask_for)
#     st.chat_message("Assitant").markdown(ai_response)
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})

#     user_input= st.chat_input("Give your response here")
#     st.chat_message("User").markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     time.sleep(25)

#     user_details, ask_for = filter_response(user_input, user_details)

#     time.sleep(25) #Gpt model doesnt allow more than 3 request per minute

st.write("Thank you for the information , we will reach out to you asap")

append_data_to_csv(user_details.__dict__)