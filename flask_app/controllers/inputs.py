from flask_app import app
from flask import render_template, request
import os
import openai
from dotenv import load_dotenv

load_dotenv()


# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/




OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
print("OPENAI API KEY:", OPENAI_KEY)
openai.api_key = OPENAI_KEY



@app.route('/openai', methods=['POST'])
def submission():
    #define input submitted from form to be used. It's the conent that will be changed to sound more like Ben wrote it
    user_input = request.form.get('input')

    #added try 
    try:
    #uses a built in function form openai installed in python
        response = openai.ChatCompletion.create(
            #setting the model to be used
            model="gpt-4",
            #argument that the API takes. You need to use a combination of role (system or user) and content to show the API what you want OpenAI to do
            messages=[
                {"role": "system", "content": "You are a helpful writing assistant. When given a topic or a short sample of writing you will produce a poem no longer than 100 words based on the content provided"},
                {"role": "user", "content": f"Please write a poem based off of {user_input}"},
                
            ]
        )
    # Extracting the assistant's reply
    #need to specify based on what's returned what you actually want to see
        assistant_reply = response['choices'][0]['message']['content']
        return assistant_reply

    except Exception as e:
        return str(e)
    
