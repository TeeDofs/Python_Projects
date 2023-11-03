import openai
import os
from dotenv import load_dotenv

load_dotenv() #Load the .env file

openai.api_key = os.getenv('OPEN_AI_API_KEY')

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Give me 3 ideas for apps I could build with openai apis "}])
print(completion.choices[0].message.content)