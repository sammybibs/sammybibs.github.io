# Contents
  - [Introduction](#introduction-)
  - [Setup](#setup-)
  - [Outcome](#outcome-)
  - [Summary](#summary-)

## Introduction <a name="introduction"></a>

9th Feb 2015

Ok I regularly change my configs in my Lab, the only variable that changes is part of the filepath & each router uses its own hostname, eg:

For dmvpn lab
```
configure replace ftp://192.168.1.251//labs/dmvpn/r1.txt
configure replace ftp://192.168.1.251//labs/dmvpn/r2.txt
configure replace ftp://192.168.1.251//labs/dmvpn/r3.txt
```

For MPLS lab
```
configure replace ftp://192.168.1.251//labs/mpls/r1.txt
configure replace ftp://192.168.1.251//labs/mpls/r2.txt
configure replace ftp://192.168.1.251//labs/mpls/r3.txt
```


Currently is am pasting the string as follows in each device
```
configure replace ftp://192.168.1.251//labs/mpls/r
```

And then on each of the 20 devices I put the final bit ```[1.txt|2.txt|3.txt]``` etc & confirm this on all (the command requires confirmation via “yes”)


Yes this works, but I really am sick of going to every box to do this several times a day, so I have looked to try to make use of TCL to save time:


## Setup <a name="setup"></a>

For my setup I have 20 CSR1000V & 1 windows VM running ftp, wireshark etc.

<br>

* Base config:

My base config on all boxes consists of an IP address, hostname & FTP credentials. After each lab I reset to this via:
```
configure replace flash:baseconfig.cfg
yes
```

* Load lab
For my scrip lab scrips, all I now need to do is send the following syntax to all devices:
```
tclsh flash:labconfig.tcl  MPLS.MP.BGP/
yes
```

TCL Script
So the script on each box is as follows (change the hostname variable on each device).

```
tclsh
puts [open flash:/labconfig.tcl w] {
 set labname [lindex $argv 0]
 set hostname "r9.txt"
 typeahead "configure replace ftp://192.168.1.251//advanced.technology.labs/${labname}${hostname}"
}
tclquit
```

## Outcome <a name="outcome"></a>
Now when you run ```tclsh flash:labconfig.tcl  MPLS.MP.BGP/``` the CLI will return the output of ```configure replace ftp://192.168.1.251//labs/dmvpn/r9.txt``` which allows us as uses to just sent one single command set to every box to load a new lab.

## Summary <a name="summary"></a>
Granted, there are lots of ways to do this. But with the resources to hand this is all i managed to conjure up and shows some use of TCL.
