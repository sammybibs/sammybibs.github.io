<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XKHR6PXZ9V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XKHR6PXZ9V');
</script>

# Contents
  - [Introduction](#introduction-)
  - [Lets explore this](#lets-explore-this-)
  - [Summary](#summary-)

## Introduction <a name="introduction"></a>
9th Feb 2015

I see this statement "For ODR to be **functional**, there should be no dynamic routing protocol configured on spokes."

Is this saying there should be no dynamic protocol over the link where ODR is running? What is meant by functional, as I have run dynamic routing and it was all working ok...


## Lets explore this <a name="lets-explore-this"></a>

* First lets check we have cdp neihgborships to run ODR over the link:

```
R5#show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R3               Tunnel0            137           R       7206VXR   Tunnel0
R1               Tunnel0            133           R       7206VXR   Tunnel0
```

* After enabling ODR we can see it's learning routing information from it's neighbours,

```
R5#show ip protocols

Routing Protocol is "odr"
  Sending updates every 60 seconds, next due in 24 seconds
  Invalid after 180 seconds, hold down 0, flushed after 240
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 4
  Routing Information Sources:
    Gateway         Distance      Last Update
    155.1.0.3            160      00:00:05
    155.1.0.1            160      00:00:09
  Distance: (default is 160)
```

* And we have their connected routes advertised to us.
```
R5#show ip route odr

      150.1.0.0/32 is subnetted, 3 subnets
o        150.1.1.1 [160/1] via 155.1.0.1, 00:00:33, Tunnel0
o        150.1.3.3 [160/1] via 155.1.0.3, 00:00:28, Tunnel0
      155.1.0.0/16 is variably subnetted, 11 subnets, 2 masks
o        155.1.13.0/24 [160/1] via 155.1.0.3, 00:00:28, Tunnel0
                       [160/1] via 155.1.0.1, 00:00:33, Tunnel0
o        155.1.37.0/24 [160/1] via 155.1.0.3, 00:00:28, Tunnel0
o        155.1.146.0/24 [160/1] via 155.1.0.1, 00:00:33, Tunnel0
```

* On the spokes we can see they have just a default route as expected, this is from the hub.

```
R1#show ip rout odr

Gateway of last resort is 155.1.0.5 to network 0.0.0.0

o*    0.0.0.0/0 [160/1] via 155.1.0.5, 00:00:35, Tunnel0
```

* Now I enable OSPF on all three devices,
>side note. The network type was set to Point-To-Multipoint as the tunnel defaults to Point-To-Point, which will not allow multiple neighbours on this interface type.)

```
!!R1-R2-R5
conf t
 router ospf 1
  network 0.0.0.0 0.0.0.0 area 0
  passive fas 0/0.100
  !
  int tun 0
  ip ospf network point-to-multipoint
!
```

* A quick verification on the hub that were ok

```
R5#show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
150.1.3.3         0   FULL/  -        00:01:34    155.1.0.3       Tunnel0
150.1.1.1         0   FULL/  -        00:01:33    155.1.0.1       Tunnel0
```

* On inspectipon of the HUBS routing table for OSR, we see nohing as expected. This is due to OSPF's AD being lower tha ODR (170 vs 110)

```
R5#show ip route odr
-nothing
```

* On the Spoke we still see the default route from the HUB.

```
R3#show ip route odr
Gateway of last resort is 155.1.0.5 to network 0.0.0.0

o*    0.0.0.0/0 [160/1] via 155.1.0.5, 00:03:42, Tunnel0
```

Ok so lets revisit the problem, accoring to the Cisco FAQ's on ODR the following is true:

**"When a spoke router sends its subnets to the hub through CDP, it checks to see if any routing protocol is enabled on the router. If it finds any dynamic routing protocol, it stops advertising its subnets."**

So lets try to lower the AD on the HUB for OSPF & see if we learn the routes & OSPF is just superseding them with it's better AD.

On Router 5 I lowered the AD for OSPF to make it higher than ODR's 170.

```
conf t
 router ospf 1
  distance 180
```

* Then just a quick bounce of the interfaces to get things converging quickly.

```
!!ALL (R1-R3-R5)
conf t
 int tun 0
  shut
  no shut

R5#show ip route odr
 nothing
```

## Summary <a name="summary"></a>
Ok, so the SPOKES are not advertising to the hub, & if we were to look on the spokes they no longer have or a default route.

The defaults that were there from ODR when we had both OSPD & ODR running were the old values aging out of the routing table.

If i remove OSPF we will learn our ODR routes again.

Thanks for tuning in.
