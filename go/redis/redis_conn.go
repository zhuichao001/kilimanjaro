package fb_redis

import (
	"fmt"
	"github.com/go-redis/redis"
)

func NewRedisClient(redisAddr string, passwd string, dbname int, poolSize int) *redis.Client {
	client := redis.NewClient(&redis.Options{
		Addr:     redisAddr,
		Password: passwd, // no password set
		DB:       dbname, // use default DB
		PoolSize: poolSize,
	})
	pong, err := client.Ping().Result()
	fmt.Println("Build Redis Pool Success.", pong, err)
	return client
}
