from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def main():
    data = {
        "name": "GOWRY N",
        "age": 21,
        "location": "KOZHIKODE"
    }
    return render_template('main.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
