# -*- coding: utf-8 -*- 

import random
import httplib
import time
import nsq
import json
import sys
import requests


class NsqWriter():
    def __init__(self, nsqd_http_hosts, topic=None):
        self.nsqd_http_hosts = nsqd_http_hosts
        self.topic = topic
        self.conn = None
        self.n = 0
        self.lasttime = 0.0
        self.__rebuild_conn()

    def __rebuild_conn(self):
        if self.conn:
            self.conn.close()

        ip, port = random.choice(self.nsqd_http_hosts).split(":")
        print "build connection: ", ip, ":", port
        self.conn = httplib.HTTPConnection(ip, int(port))
        self.lasttime = time.time()

    def __inc_n(self, num):
        self.n += num
        if self.n % 200 ==0 or time.time()-self.lasttime>30:
            self.__rebuild_conn()
        self.lasttime = time.time()

    def produce_old(self, msg=None, topic=None):
        if not msg:
            print "Error, call produce, msg:", msg
            return

        topic = topic or self.topic
        if topic is None:
            print "Error, call produce, topic is None"
            return

        try:
            self.__inc_n(1)
            self.conn.request("POST", "/pub?topic="+topic, msg, {"Contention":"Keep-Alive"})
            response = self.conn.getresponse()
            print response.read(), topic
        except Exception, e:
            print "Exception: ", e
            self.__rebuild_conn()

    def produce(self, msg=None, topic=None):
        if not msg:
            print "Error, call produce, msg:", msg
            return

        topic = topic or self.topic
        if topic is None:
            print "Error, call produce, topic is None"
            return

        try:
            host = random.choice(self.nsqd_http_hosts)
            url = "http://" + str(host) + "/pub?topic=" + topic
            r = requests.post(url, data=msg)
            print r.text, topic
        except Exception, e:
            print "Exception: ", e

    def mproduce(self, msgs):
        if not msgs or not ( isinstance(msgs, list) or isinstance(msgs, tuple) ):
            print "ERROR: call mproduct, msgs=", msgs
            return
        try:
            result = []
            for msg in msgs:
                result.append(json.dumps(msg) if isinstance(msg, dict) else str(msg)) 
            host = random.choice(self.nsqd_http_hosts)
            url = "http://" + str(host) + "/mpub?topic=" + self.topic
            r = requests.post(url, data="\n".join(result))
            print r.text, self.topic
        except Exception, e:
            print "Exception: ", e
 
    def mproduce_old(self, msgs):
        if not msgs or not ( isinstance(msgs, list) or isinstance(msgs, tuple) ):
            print "ERROR: call mproduct, msgs=", msgs
            return
        try:
            self.__inc_n(1)
            result = []
            for msg in msgs:
                result.append(json.dumps(msg) if isinstance(msg, dict) else str(msg))
            self.conn.request("POST", "/mpub?topic="+self.topic, '\n'.join(result), {"Contention":"Keep-Alive"})
            response = self.conn.getresponse()
            print response.read()
        except Exception, e:
            print "Exception: ", e
            self.__rebuild_conn()


class NsqReader():
    def __init__(self, lookupd_http_addresses, topic, channel, handler, max_in_flight=20):
        self.r = nsq.Reader(message_handler=handler, 
            lookupd_http_addresses=lookupd_http_addresses, 
            topic=topic, channel=channel, max_in_flight=max_in_flight, max_tries=3)

    def run(self):
        nsq.run()


if __name__ == "__main__":
    w = NsqWriter(["localhost:4151", "localhost:4251", "localhost:4151"])
    topic = "hot_news"
    msg = '{"title": "xxxx", "content":"yyyy"}'
    w.produce(msg, topic)
