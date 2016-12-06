from flask import Flask, render_template, json, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()


resp = request.get('index.html')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for todo_item in resp.json():
    print('{} {}'.format(todo_item['id'], todo_item['summary']))
