# TOC
- [Diagnostics Question](#DiagnosticsQuestion)
  - [Reported issue](#Reportedissue)
    - [Initial Pings](#InitialPings)
      - [Client 1](#Client1)

# Diagnostics Question <a name="DiagnosticsQuestion"></a>
December 14 2016

Your job is to diagnose & locate the source of the problem, please post your comments below & I will follow this up with a post detailing the solution in due course.

The following is the topology for BlogTown's new network that has just been installed. It is made up of three multilayer switches. The core switch 'Switch 2'  provides layer three access to various services, such as the Internet & internal servers.

The two clients that connected to Switch 1 & Switch 3 are both in the same VLAN & subnet '192.168.1.0/24'

![](images/2023-01-06-13-59-06.png)


## Reported issue <a name="Reportedissue"></a>
The users of the clients have complained that they cannot communicate directly with one another, but they can reach thier local IP hateways

Troubleshooting already completed:
Ping tests were run from both client PC's to test reachability. Following this a second ping test was run to see if either client could reach the Internet facing port Eth1/1 on Switch 2, results can be seen below in the log file 'Initial Pings".

Further Information Requested:
To help isolate the fault the following items were asked for & can be seen below:

- "show run" from all three switches
- "show vtp status" from all three switches
- "show vlan" from switches 1 & 3
- "show spanning-tree" from switch 1
- "show log" from switch 2

### Initial Pings <a name="InitialPings"></a>
#### Client 1 <a name="Client1"></a>
```
!!!Ping Swithc 1 SVI gateway for Client 1
CLIENT1#ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 5/5/5 ms

!!!Ping Client 2 IP
CLIENT1#ping 192.168.1.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.2, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)

!!!Ping Switch 2 Eth 1/1 WAN interface
CLIENT1#ping 192.168.255.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.255.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```
