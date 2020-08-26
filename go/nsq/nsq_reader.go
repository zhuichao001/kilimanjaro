package nsq

import (
	_ "errors"
	"fmt"
	"github.com/nsqio/go-nsq"
	_ "strings"
	"time"
)

type NsqReader struct {
	nsqd_hosts []string
	consumer   *nsq.Consumer
}

func (r *NsqReader) Run(nsqds []string, topic string, channel string, handler nsq.Handler, maxinflight int) {
	cfg := nsq.NewConfig()
	cfg.LookupdPollInterval = time.Second
	cfg.MaxInFlight = maxinflight

	rd, err := nsq.NewConsumer(topic, channel, cfg)
	if err != nil {
		panic(err.Error())
	}

	rd.AddHandler(handler)
	rd.ConnectToNSQDs(nsqds)
	r.consumer = rd
}
