package db

import (
	"database/sql"
	"fmt"
)

func OpenDB(driver string, dbUrl string) *sql.DB {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("OpenDB Recover!!!")
		}
	}()

	dbpool, err := sql.Open(driver, dbUrl) //driver(default):"mysql"
	if err != nil {
		panic(err)
	}
	return dbpool
}
