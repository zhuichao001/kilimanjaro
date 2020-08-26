package datetime

import (
	"fmt"
	"time"
)

func TimeNow() string {
	return time.Now().Format("2006-01-02 15:04:05")
}

func TimeAgo(s string) string {
	now := time.Now()
	t, _ := time.ParseDuration(s)
	t1 := now.Add(t)
	return t1.Format("2006-01-02 15:04:05")
}

func GetDayStart() string {
	return time.Now().Format("2006-01-02 00:00:00")
}
