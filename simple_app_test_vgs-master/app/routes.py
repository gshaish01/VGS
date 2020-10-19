from app import app
from flask import render_template, request, jsonify
import requests
import os
import json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')




@app.route("/forward", methods=['POST'])
def forward():
    cc_cvv = request.form['cc_cvv']
    cc_number = request.form['cc_number']
    cc_exp = request.form['cc_exp']


    response_i = requests.post("https://tntsvizavbe.sandbox.verygoodproxy.com//post",
                             json={'cvv': cc_cvv, 'card_number': cc_number, 'exp_date': cc_exp})
    #print(str(response_i.text))
    response_i=response_i.json()
    J_card_number=(json.dumps(response_i['json']['card_number'], indent=4).strip('"'))
    J_cvv=(json.dumps(response_i['json']['cvv'],  indent=4).strip('"'))
    J_exp_date=(json.dumps(response_i['json']['exp_date'],  indent=4).strip('"'))




    os.environ[
        'HTTPS_PROXY'] = '{user:password}@tntsvizavbe.sandbox.verygoodproxy.com:8080'
    response = requests.post('https://echo.apps.verygood.systems/post',
                             json={'cvv': J_cvv, 'card_number': J_card_number, 'exp_date': J_exp_date },
                             verify='sandbox.pem')

    #print(str(response.text))
    response = response.json()



    return render_template('forward.html', response=response,response_i=response_i)
