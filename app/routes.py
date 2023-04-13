from app import app
from flask import send_file, request, jsonify
from app.helper import analyze_business
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/download_sample')
def download_sample():
    filename = "/home/skylot/Documents/business/sample.xlsx"
    return send_file(filename, as_attachment=True)


@app.route('/analyze', methods = ['POST'])
def analyze():
    uploaded_file = request.files['file']
    res = analyze_business(uploaded_file)
    print(res)
    response = jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=res)

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
