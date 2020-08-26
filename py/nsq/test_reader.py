#encoding:utf-8


import pyutil.nsq.config.conf_ol as conf_ol
import pyutil.nsq.nsqer as nsqer
import pyutil.fb_gevent.gevent_util as gevent
import time

@gevent.gevent_handler
def handler(msg):
    print msg.id, msg.body
    time.sleep(100)
    return True

if __name__ == '__main__':
    reader = nsqer.NsqReader(conf_ol.config["nsqlookupd_http_hosts"], "test_nsq_by_zhc", "zhc_chan1", handler)
    reader.run()
