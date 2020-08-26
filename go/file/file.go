package file

import (
	"fmt"
	"os"
)

func Mkdir(path string) {
	_, err := os.Stat(path)
	if err != nil {
		if os.IsNotExist(err) {
			err := os.Mkdir(path, os.ModePerm)
			if err != nil {
				panic(fmt.Sprintf("Mkdir failed![%v], path:%s\n", err, path))
			}
		}
	}
	return
}
