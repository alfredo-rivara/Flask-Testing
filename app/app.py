from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1 id="welcome-message">Mining Consulting QA Testing</h1>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)

