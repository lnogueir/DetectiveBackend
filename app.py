

from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

## FIRST LECTURE ##

# @app.route('/')
# def home():
#     print('Something...') # Se eu printo aqui, sempre que eu der um GET
#     return '{"jobs":[ 1,2,3,4]}'# eu vou printar Something...

# // #       # // #


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/game')
def game():
    return render_template("game.html")


app.run(port=5000)
