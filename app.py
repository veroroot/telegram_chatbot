from flask import Flask, escape, request, render_template
from decouple import config
import requests
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
google_key = config('GOOGLE_TRANSLATE_KEY')
weather_key = config('OPEN_WEATHERMAP_KEY')

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
    print(response)
    user_id = response['result'][0]['message']['from']['id']

    user_input = request.args.get("user_input")

    send_url=f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={user_input}"
    requests.get(send_url)

    return render_template('send.html')

# web hook 개발 테스트(실제할 때에는 token을 주소값으로 사용하는 것을 추천한다.)
@app.route('/telegram', methods=['POST'])
def telegram():
    req = request.get_json()
    user_id = req['message']['from']['id']
    user_input = req['message']['text']

    chat_function = ['로또', '날씨', '번역']
    

    if user_input == "로또":
        # 1부터 45까지 숫자를 저장한다.
        numbers = list(range(1,46))
        # 그중 6개를 뽑는다.
        lucky = random.sample(numbers, 6)
        # 정렬하기
        sorted_lucky = sorted(lucky)
        lucky_answer = f"행운의 숫자는 : {sorted_lucky}"
        return_data = lucky_answer

    elif user_input == "날씨":
        url = 'https://api.openweathermap.org/data/2.5/weather?q=Seoul,kr&lang=kr&appid='+weather_key

        data = requests.get(url).json()
        weather = data['weather'][0]['main']
        temp = float(data['main']['temp'])-273.15
        temp_min = float(data['main']['temp_min'])-273.15
        temp_max = float(data['main']['temp_max'])-273.15

        return_data = '''
        서울의 오늘 날씨는 {}이며,\n현재 기온은 {:.1f}도 입니다.\n최저/최고 온도는 {:.1f}/{:.1f}입니다.'''.format(weather, temp, temp_min, temp_max)

    elif user_input == "번역" :
        return_data = '[번역 번역대상] []안의 형태로 입력하여 주십시오'

    elif user_input[0:3] == "번역 ":
        google_api_url="https://translation.googleapis.com/language/translate/v2"
        before_text = user_input[3:]

        data = {
            'q' : before_text,
            'source' : 'ko',
            'target' : 'en'
        }
        request_url = f'{google_api_url}?key={google_key}'

        response = requests.post(request_url, data).json()
        #print(response)

        return_data = response['data']['translations'][0]['translatedText']

    elif user_input == "점심식사":
        url = 'https://www.siksinhot.com/taste?upHpAreaId=9&hpAreaId=1122'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #tabMove1 > div > ul > li:nth-child(1) > div > a > div > div > strong
        key_selector = '#tabMove1 > div > ul > li > div > a > div > div > strong'
        keys = soup.select(key_selector)
        #print(keys)
        key_list = [key.text for key in keys]
        #print(key_list)
        #tabMove1 > div > ul > li:nth-child(1) > div > a > span > img
        img_selector = '#tabMove1 > div > ul > li > div > a > span > img'
        imgs = soup.select(img_selector)
        #print(imgs)
        img_list = [img.get('src') for img in imgs]
        #print(img_list)
        
        menu=dict(zip(key_list, img_list))
        
        #menu_select = random.choice(menu)
        #return_data = menu_select

    else :
        return_data = f"지금 사용가능한 명령어는 {chat_function}입니다."

    send_url=f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={return_data}"
    requests.get(send_url)

    return 'ok', 200

if __name__=='__main__':
    app.run(debug=True)