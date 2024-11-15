from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template('index.html')
# def index():
#     return "index"

# if __name__== "__main__":
app.run(debug=True)
    

# @app.