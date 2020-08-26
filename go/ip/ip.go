package ip

import (
	"errors"
	"fmt"
	"net"
)

func IpAddress() (string, error) {
	all, err := net.InterfaceAddrs()
	if err != nil {
		fmt.Println(err)
		return "-", err
	}

	for _, address := range all {
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				return ipnet.IP.String(), nil
			}
		}
	}
	return "-", errors.New("Not found local ipnet.")
}
