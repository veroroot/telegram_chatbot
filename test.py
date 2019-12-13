import requests
from decouple import config

# Telegram chatbot key를 가져온다.
token = config('TELEGRAM_BOT_TOKEN')

url = f'https://api.telegram.org/bot{token}/getUpdates'
#print(url)

#response = requests.get(url).text
# response 형태는 str -> parse -> dict
response = requests.get(url).json()
#print(response)

user_id = response['result'][0]['message']['from']['id']
#print(user_id)

user_input = input("보낼메시지를 입력해주세요 : ")

send_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={user_input}'

requests.get(send_url)