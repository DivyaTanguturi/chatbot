import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_ttps_context=ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

#Load intents from json file
file_path=os.path.abspath("./intents.json")
with open(file_path,"r") as file:
    intents=json.load(file)

#create the vectorizer and classifier
vectorizer=TfidfVectorizer()
clf=LogisticRegression(random_state=0,max_iter=10000)

#preprocess the data
tags=[]
patterns=[]
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

#Training the model
x= vectorizer.fit_transform(patterns)
y=tags
clf.fit(x,y)

def chatbot(input_text):
    input_text=vectorizer.transform([input_text])
    tag=clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag']==tag:
            response=random.choice(intent['responses'])
            return response
counter=0


def main():
    global counter
    st.title("Intents of chatbot using NLP")

    #Create a sidebar menau with options
    menu=["Home","Converstion History","About"]
    choice=st.sidebar.selectbox("Menu",menu)

    #Home menu
    if choice == "Home":
        st.write("Welcom to the chatbot.Please type a message and press eneter to start the converstion")

        #check if the chat_log.csv file exists, and if not, create it with column names
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv','w',newline='', encoding='utf-8') as csvfile:
                csv_writer=csv.writer(csvfile)
                csv_writer.writerow(['User Input','Chatbot Response','Timestamp'])
                
        counter+=1
        user_input=st.text_input("you:",key=f"user_input_(counter)")

        if user_input:
            
            #convert the user input to a string
            user_input_str=str(user_input)

            response=chatbot(user_input)
            print("Response:", response)
            st.text_area("Chatbot:", value=response, height=120,max_chars=None, key=f"chatbot")

            #get the current time stamp
            timestamp=datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

            #save the user input and chatbot response to the chat_log.csv file
            with open('chat_log.csv','a',newline='',encoding='utf-8') as csvfile:
                csv_writer=csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['goodbye','bye']:
                      st.write("Thank you fot chatting with me. Have a greate day!")
                      st.stop()

    #conversation History Menu
    elif choice=="Conversation History":
        #Display the conversation history in a collapsiable expander
        st.header("Conversation History")
        #with st.beta expander("click to see Converstion Hisory")
        with oepn('chat_log.csv','r',ecoding='utf-8') as csvfile:
            csv_reader=csv.reader(csvfile)
            next(csv_reader)#skip the header row
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    elif choice=="About":
        st.write("The goal of this project is to create a chatbot that can unserstand and response to human Quries in natural language")

        st.subheader("Project Overview")
        st.write("A chatbot using Natural Language Processing (NLP) leverages AI techniques to understand,interpret, and respond to human language. It analyzes text inputs through processes like tokenization, parsing, and intent recognition to generate meaningful responses. NLP-powered chatbots are widely used in customer service, virtual assistants, and automation systems.")

        st.subheader("Dataset:")
        st.write("The data set used in this project is a collection of labeled intents and entities. The intents of the user input are like 'greeting', 'about'. The entities extracted from user input.")


        st.subheader("Sreamlit chatbot interface:")
        st.write("The chatbot interface is built using streamlit.Streamlit is an open-source Python library that allows users to create interactive web applications with minimal code. It provides an intuitive interface for building data-driven applications, visualizations, and machine learning tools.")

      
        st.subheader("Conclusion:")
        st.write("In this project a chatbot is built that can understand and respond to user user input")

if __name__=='__main__':
    main()

            
                


























    
