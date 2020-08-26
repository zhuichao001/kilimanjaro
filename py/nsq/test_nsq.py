
import json
from pyutil.nsq.nsqer import NsqWriter
from pyutil.nsq.config import conf_ol


def test():
    writer = NsqWriter(conf_ol.config["nsqd_http_hosts"], "maint_notification_test")
    msg = {"abc":123}
    writer.produce(json.dumps(msg))

if __name__ == '__main__':
    test()
