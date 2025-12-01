# Author : ysh
# 2025/11/17 Mon 17:43:49
from core.general import *
from lib.general import *

import lib.model as model
import lib.game

from flask import Blueprint, send_file, make_response, request
import requests
import json

app = Blueprint('model', __name__)

@app.route('/model/ask_llm', methods = ['GET', 'POST'])
def ask_llm():
    info(f'Received Request sent from {request.remote_addr}')
    return ok(model.ask_llm(request.values['data']))

@app.route('/game/get_category', methods = ['GET', 'POST'])
def get_category():
    if not require(request, ['rules']):
        return fail('Key missing')
    
    rules = request.values['rules']

    ans = (lib.game.get_category(rules))
    if ans is None:
        return fail('Model Failed')
    
    return ok(category = ans[0], faith = ans[1], trial = ans[2])

@app.route('/game/get_strategy', methods = ['GET', 'POST'])
def get_strategy():
    if not require(request, ['rules']):
        return fail('Key Missing')
    
    rules = request.values['rules']

    ans = lib.game.get_strategy(rules)
    if ans is None:
        return fail('Model Failed')
    
    return ok(ans)
