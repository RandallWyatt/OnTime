from flask import Flask, render_template, json, request

app = Flask(__name__)


@app.route('/', defaults={'color': 'default'})
@app.route('/<color>', endpoint='color')
def main(color):
    style_link = '/static/' + color + '.css'
    return render_template('index.html', styles=style_link)

if __name__ == '__main__':
    app.run()


