from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    cards = [{'card_img': '/static/imgs/card1.jpg',
              'card_title': 'Заголовок карты1',
              'card_text': 'Текст карты1',
              'card_btn_name': 'Кнопка1'},
             {'card_img': '/static/imgs/card2.jpg',
              'card_title': 'Заголовок карты2',
              'card_text': 'Текст карты2',
              'card_btn_name': 'Кнопка2'},
             {'card_img': '/static/imgs/card3.jpg',
              'card_title': 'Заголовок карты3',
              'card_text': 'Текст карты3',
              'card_btn_name': 'Кнопка3'},
             ]
    context = {'title': 'Интернет магазин одежды и обуви',
               'greetings': 'Распродажа в интернет-магазине',
               'cards': cards}
    return render_template('index9.html', **context)

@app.route('/shoes/')
def shoes():
    shoes = [{'card_img': '/static/imgs/shoes1.jpg',
              'card_title': 'Заголовок ботинок1',
              'card_text': 'Текст ботинок1',
              'card_btn_name': 'Кнопка1'},
             {'card_img': '/static/imgs/shoes2.jpg',
              'card_title': 'Заголовок ботинок2',
              'card_text': 'Текст ботинок2',
              'card_btn_name': 'Кнопка2'},
             {'card_img': '/static/imgs/shoes3.jpg',
              'card_title': 'Заголовок ботинок3',
              'card_text': 'Текст ботинок3',
              'card_btn_name': 'Кнопка3'},
             ]
    context = {'title': 'Интернет магазин одежды и обуви',
               'greetings': 'Каталог обуви',
               'cards': shoes}
    return render_template('shoes.html', **context)

@app.route('/jackets/')
def jackets():
    jackets = [{'card_img': '/static/imgs/card1.jpg',
              'card_title': 'Заголовок одежды1',
              'card_text': 'Текст одежды1',
              'card_btn_name': 'Кнопка1'},
             {'card_img': '/static/imgs/card2.jpg',
              'card_title': 'Заголовок одежды2',
              'card_text': 'Текст одежды2',
              'card_btn_name': 'Кнопка2'},
             {'card_img': '/static/imgs/card3.jpg',
              'card_title': 'Заголовок одежды3',
              'card_text': 'Текст одежды3',
              'card_btn_name': 'Кнопка3'},
             ]
    context = {'title': 'Интернет магазин одежды и обуви',
               'greetings': 'Каталог одежды',
               'cards': jackets}
    return render_template('jackets.html', **context)

if __name__ == "__main__":
    app.run()