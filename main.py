import pandas as pd
import requests
import json
import openai

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = 'sk-todo'
openai.api_key = openai_api_key

df = pd.read_csv('userId.cvs')
user_ids = df['userId'].tolist()
users = [user for id in user_ids if (user := get_user(id)) is not None]
for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")


def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')