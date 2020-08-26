#encoding:utf-8


import pyutil.nsq.config.conf_ol as conf_ol
import pyutil.nsq.nsqer as nsqer

topic = "test"
hosts = ["36.110.189.22:4151", "36.110.189.22:4251"] 

def test():
    writer = nsqer.NsqWriter(hosts, topic)
    import json
    data = {"uuid":"b6122db1-5d33-44e7-83ef-9cc15a3e583d","dtuId":65979288061713,"alarmHostId":1,"thingId":88061713012134001,"componentCode":12134,"thingType":"info_device_component","thingTypeId":40,"statusId":2,"position":"","receiveTime":"2019-03-19 11:30:33","hostTime":"2019-03-19 11:30:33","value":"","valueOrig":"","valueType":1,"loopNumber":-1,"componentNumber":-1,"protocol":"Rtu","errorCode":2}
    msg = json.dumps(data)
    writer.produce(msg)

if __name__ == '__main__':
    #writer = nsqer.NsqWriter(conf_ol.config["nsqd_http_hosts"], "test_nsq_by_zhc")
    #for i in range(1000):
    #    writer.produce("hello, zhc, msg001")
    #    writer.mproduce(["hello, msg 002", "hello, msg 003"])
    test()
