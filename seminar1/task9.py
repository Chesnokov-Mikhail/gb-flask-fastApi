from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    cards = [{'card_img': 'картинка1',
              'card_title': 'Заголовок карты1',
              'card_text': 'Текст карты1',
              'card_btn_name': 'Кнопка1'},
             {'card_img': 'картинка2',
              'card_title': 'Заголовок карты2',
              'card_text': 'Текст карты2',
              'card_btn_name': 'Кнопка2'},
             {'card_img': 'картинка3',
              'card_title': 'Заголовок карты3',
              'card_text': 'Текст карты3',
              'card_btn_name': 'Кнопка3'},
             ]
    context = {'title': 'Интернет магазин одежды',
               'greetings': 'Распродажа в интернет-магазине',
               'cards': cards}
    return render_template('index9.html', **context)

if __name__ == "__main__":
    app.run()