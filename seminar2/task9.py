from flask import Flask, render_template, request, url_for, make_response, redirect

# Создать страницу, на которой будет форма для ввода имени и электронной почты,
# при отправке которой будет создан cookie-файл с данными пользователя,
# а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл
# с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты.

app = Flask(__name__)
# app.secret_key = 'a18dd37767c54faf75ee2fb5298aad8cc753eba70d8b42efca0aae1d1dea9434'

@app.route('/')
def index():
    content = {'title': 'Страница входа',
               'name_form': 'Введите имя и электронную почту'}
    return render_template('send_form.html', **content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        context = {'title': 'Успешный вход',
                   'text': 'Добро пожаловать ',
                   'name': request.form.get('username').capitalize(),
                   }
        response = make_response(render_template('welcome.html', **context))
        response.set_cookie('username', request.form.get('username'))
        response.set_cookie('email', request.form.get('email'))
        return response
    return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        content = {'title': 'Страница входа',
                   'name_form': 'Введите имя и электронную почту',
                   }
        response = make_response(render_template('send_form.html', **content))
        response.delete_cookie('username')
        response.delete_cookie('email')
        return response
    else:
        if request.cookies.get('username'):
            context = {'title': 'Успешный вход',
                        'text': 'Добро пожаловать ',
                        'name': request.cookies.get('username').capitalize(),
                        }
            response = make_response(render_template('welcome.html', **context))
            return response
        else:
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)