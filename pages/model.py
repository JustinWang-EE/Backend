# Author : ysh
# 2025/11/17 Mon 17:43:49
from core.general import *
from lib.general import *

import lib.model as model

from flask import Blueprint, send_file, make_response, request
import requests
import json

app = Blueprint('model', __name__)

@app.route('/model/ask_llm', methods = ['GET', 'POST'])
def ask_llm():
    info(f'Received Request sent from {request.remote_addr}')
    return ok(model.ask_llm(request.values['data']))