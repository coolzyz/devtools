#/bin/env python3

import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

#curl -H "Content-type: application/json" -X POST -d '{"cmd": "changetime", "totime": "2022-10-31 9:58:58"}' "http://10.240.131.207:9002"


class Resquest(BaseHTTPRequestHandler):
    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())


    def do_POST(self):
        #print("header:", self.headers)
        #print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length'])) 
        content = json.loads(req_datas.decode())
        print(content)

        data = {
            'result': '',
            'cur_time': '',
        }

        if content['cmd'] == 'changetime':
            try:
                do_change_time(content['totime'])
            except ValueError as e:
                data['result'] = str(e)
            else:
                data['result'] = 'Success'

        else:
            data['result'] = 'not supported'

        data['cur_time'] = str(datetime.now())

        data = { key : data[key] for key in sorted(data.keys(), reverse = True) }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

'''
    str format : 2022-10-10 10:00:00
'''
def do_change_time(to:str):
    try:
        doj = datetime.strptime(to, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise ValueError("Failed! {0}".format(str(e)))
    else:
        if doj < datetime.now():
            raise ValueError("Failed! input time should be greater than current time")

        cmd = 'date -s {0}'.format(to)
        print("start change time cmd:", cmd)
        os.system(cmd)




if __name__ == '__main__':
    host = ('', 9002)
    server = HTTPServer(host, Resquest)
    print("starting server, listen on: %s:%s" % host)
    server.serve_forever()

