# Author : ysh
# 2025/11/17 Mon 17:37:07
from core.general import *
from lib.general import *

from flask import Blueprint, send_file, make_response, request
import requests
import json

app = Blueprint('test', __name__)

@app.route('/echo', methods = ['GET'])
def echo():
    print(request.values)
    return request.values