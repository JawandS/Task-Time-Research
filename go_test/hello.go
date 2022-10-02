package main

import (
	"C"

	bpf "github.com/aquasecurity/tracee/libbpfgo"
)
import (
	"fmt"
	"os"
	"os/signal"
)

func main() {
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)

	bpfModule, err := bpf.NewModuleFromFile("hello.bpf.o")
	checkErr(err)
	defer bpfModule.Close()

	err = bpfModule.BPFLoadObject()
	checkErr(err)

	prog, err := bpfModule.GetProgram("hello")
	checkErr(err)
	_, err = prog.AttachKprobe(sys_execve)
	checkErr(err)

	go bpf.TracePrint()
}

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}