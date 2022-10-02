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
	must(err)
	defer bpfModule.Close()

	err = bpfModule.BPFLoadObject()
	must(err)

	prog, err := bpfModule.GetProgram("hello")
	must(err)
	_, err = prog.AttachKprobe(sys_execve)
	must(err)

	go bpf.TracePrint()
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}