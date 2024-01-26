from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    context = {'title': 'Моя первая страница на Flask',
               'contents': 'Здравствуйте! Начальная страница моего первого сайта на Flask'}
    return render_template('index8.html', **context)


@app.route('/about/')
def about():
    context = {'title': 'О нас',
               'contents': {'name': 'Студенты GB, курса "Фреймворки Flask и FastAPI"',
                            'students': ['Иванов', 'Петров', 'Васечкин'],  }
               }
    return render_template('about.html', **context)

@app.route('/contact/')
def contact():
    contacts = [{'Адрес': 'Челябинск',
                'Телефон': 1278457887,
                'e-mail': 'info@home.ru',
                'Время работы': '09:00 - 18:00, пн.-пт.'}]
    context = {'title': 'Контакты',
               'contents': {'description': 'Контакты',
                            'contacts': contacts,}
               }
    return render_template('contact.html', **context)

if __name__ == '__main__':
    app.run()
