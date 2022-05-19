#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :main.py
@说明    :
@时间    :2020/12/08 20:38:24
@版本    :1.0
'''
import logging
import random
import re
from logging.handlers import TimedRotatingFileHandler
import pandas as pd

from flask import Flask, render_template, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
logger = logging.getLogger('werkzeug')
logging.basicConfig(level=logging.INFO)
# 按天切分日志
handler = TimedRotatingFileHandler(filename='info.log', when='midnight', backupCount=7, encoding='utf-8')
handler.suffix = '%Y-%m-%d.log'
handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
logger.addHandler(handler)
app.logger.addHandler(handler)

CORS(app, supports_credentials=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    r = random.randint(0, 65535)
    logger.info("INFO:"+str(r) + " " + request.remote_addr + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return render_template('index.html', random=r)


@app.route('/static/css/style.css', methods=['POST', 'GET'])
def style():
    r1 = random.randint(0, 255)
    r2 = random.randint(0, 255)
    #logging.info("random: {}".format(r1 * 256 + r2))
    return render_template('style.css', random1=r1, random2=r2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
