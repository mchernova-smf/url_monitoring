from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    with open("output/dashboard.html", "r") as f:
        html_page = f.read()
    return html_page

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')