from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    get_user_api = f"{api_url}/bot{token}/getUpdates"
    response = requests.get(get_user_api).json()
    user_id = response['result'][0]['message']['from']['id']

    user_input = request.args.get("user_input")

    send_url=f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={user_input}"
    requests.get(send_url)

    return render_template('send.html')

# web hook 개발 테스트(실제할 때에는 token을 주소값으로 사용하는 것을 추천한다.)
@app.route('/telegram', methods=['POST'])
def telegram():
    
    return 'ok', 200

if __name__=='__main__':
    app.run(debug=True)