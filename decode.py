from datetime import datetime


file_handle = open('msg.txt', mode='w')

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

dic = ['','00', '01', '11', '10']
keys = [0, 1, 4, 1, 1, 1, 1, 1, 1]
for key, value in ipd.items():
    if len(value) > 9:
        flag = True
        for i in range(1, 9):
            if value[i] != keys[i]:
                flag = False
                break
        if flag:
            msg = ""
            for i in range(9, len(value)):
                msg += dic[value[i]]
            file_handle.write(msg+'\n')
