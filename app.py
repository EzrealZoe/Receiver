#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@说明    :
@时间    :2020/12/08 20:38:24
@版本    :1.0
'''
import logging
import random
import re
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template, request, send_from_directory
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
    logger.info("INFO:" + str(r) + " " + request.remote_addr + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return render_template('index.html', random=r)


@app.route('/static/css/style.css', methods=['POST', 'GET'])
def style():
    r1 = random.randint(0, 255)
    r2 = random.randint(0, 255)
    # logging.info("random:  {}".format(r1 * 256 + r2))
    return render_template('style.css', random1=r1, random2=r2)


@app.route('/compute', methods=['POST', 'GET'])
def compute():
    file_handle = open('msg.txt', mode='w')



    ipd = []
    for line in open("info.log", "r", encoding='UTF-8'):
        i += 1
        if 'INFO:' in line:
            line = line[5:]
            i = 1
            while line[i] != " ":
                i += 1
            num = int(line[:i])
            line = line[i + 1:]
            i = 1
            while line[i] != " ":
                i += 1
            ip = line[:i]
            t = datetime.strptime(line[i + 1:-1], '%Y-%m-%d %H:%M:%S.%f')
            if i == 1:
                ipd = [t]
            interval = round((t - ipd[0]).total_seconds() / 10)
            if interval > 4:
                ipd.append(4)
            elif interval == 0:
                ipd.append(1)
            else:
                ipd.append(interval)
            ipd[0] = t


    dic = ['', '00', '01', '11', '10']
    keys = [0, 1, 4, 1, 1, 1, 1, 1, 1]
    ret = ""
    for i in range(len(ipd)):
         msg = ""
         msg += dic[ipd[i]]
    file_handle.close()
    return {"code": 200, "data": msg}


@app.route('/res', methods=['POST', 'GET'])
def res():
    try:
        return send_from_directory('', filename='res.log', as_attachment=True)
    except Exception as r:
        return '<h1>该文件不存在或无法下载</h1>'


@app.route('/msg', methods=['POST', 'GET'])
def msg():
    try:
        return send_from_directory('', filename='msg.txt', as_attachment=True)
    except Exception as r:
        return '<h1>该文件不存在或无法下载</h1>'


@app.route('/info', methods=['POST', 'GET'])
def info():
    try:
        return send_from_directory('', filename='info.log', as_attachment=True)
    except Exception as r:
        return '<h1>该文件不存在或无法下载</h1>'


@app.route('/clear', methods=['POST', 'GET'])
def clear():
    file_handle = open('msg.txt', mode='w')
    file_handle.write(' ')
    file_handle.close()
    return {"code": 200}


@app.route('/display', methods=['POST', 'GET'])
def display():
    ipd = {}
    for line in open("info.log", "r", encoding='UTF-8'):
        if 'INFO:' in line:
            line = line[5:]
            i = 1
            while line[i] != " ":
                i += 1
            num = int(line[:i])
            line = line[i + 1:]
            i = 1
            while line[i] != " ":
                i += 1
            ip = line[:i]
            t = datetime.strptime(line[i + 1:-1], '%Y-%m-%d %H:%M:%S.%f')
            if ipd.get(ip):
                interval = round((t - ipd[ip][0]).total_seconds() / 10)
                if interval > 4:
                    ipd[ip].append(4)
                elif interval == 0:
                    ipd[ip].append(1)
                else:
                    ipd[ip].append(interval)
                ipd[ip][0] = t
            else:
                ipd[ip] = [t]
    return {"code": 200, "data": ipd}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
