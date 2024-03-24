from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main():
    return render_template('templates/html/first_page.html')


if __name__ == '__main__':
    app.run("", 8080)
