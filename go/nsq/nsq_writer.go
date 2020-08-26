package nsq

import (
	"errors"
	"fmt"
	"github.com/nsqio/go-nsq"
	"math/rand"
	"strings"
	"time"
)

type NsqWriter struct {
	Host     string
	Producer *nsq.Producer
	Messages chan [2]string
}

var nsqdHosts []string
var nsqers []*NsqWriter

var R *rand.Rand

func InitNsq(nsqd string) {
	R = rand.New(rand.NewSource(time.Now().UnixNano()))
	nsqdHosts = strings.Split(nsqd, ",")
	nsqers = make([]*NsqWriter, len(nsqdHosts))

	for i, host := range nsqdHosts {
		nsqers[i] = &NsqWriter{
			Host:     host,
			Messages: make(chan [2]string),
		}

		go func(idx int) {
			for {
				item := <-nsqers[idx].Messages
				nsqers[idx].Publish(item[0], item[1])
			}
		}(i)
	}
}

func PushToNsq(topic string, msg string) {
	nsqers[R.Intn(len(nsqers))].Messages <- [2]string{topic, msg}
}

func (nsqer *NsqWriter) Publish(topic string, message string) error {
	if nsqer.Producer == nil {
		fmt.Println("Init NsqWriter, Host: ", nsqer.Host)

		var err error
		if nsqer.Producer, err = nsq.NewProducer(nsqer.Host, nsq.NewConfig()); err != nil {
			fmt.Println("Error: producer is nil")
			return err
		}
	}

	if topic == "" {
		err_msg := "Error: NsqWriter Publish topic is empty"
		fmt.Println(err_msg)
		return errors.New(err_msg)
	}

	if message == "" {
		err_msg := "Error: NsqWriter Publish message is empty"
		fmt.Println(err_msg)
		return errors.New(err_msg)
	}

	if err := nsqer.Producer.Publish(topic, []byte(message)); err != nil {
		PushToNsq(topic, message)

		err_msg := "Error: NqqWriter Publish message failed"
		fmt.Println(err_msg, topic, message)

		nsqer.Producer.Stop()
		nsqer.Producer = nil
		return errors.New(err_msg)
	} else {
		fmt.Println("host:", nsqer.Host, "|||NSQ PRODUCE SUCCESS, topic:", topic, ", message:", message)
	}
	return nil
}
