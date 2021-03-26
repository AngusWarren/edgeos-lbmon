package main

/* This app just executes "/usr/sbin/ubnt-hal wlbGetWdStatus"
   and sends the output to stdout. Setting the SUID bit on this file 
   allows non-admin users to get this output safely.

   Compile for Ubiquiti routers using miplsle and mips64.
   GOARCH=mips64 GOOS=linux go build -ldflags="-s -w" show-watchdog-status.go
   GOARCH=mipsle GOOS=linux go build -ldflags="-s -w" show-watchdog-status.go
*/

import (
    "os"
    "os/exec"
)

func main() {
    out, _ := exec.Command("/usr/sbin/ubnt-hal", "wlbGetWdStatus").Output()
    os.Stdout.WriteString(string(out))
}

