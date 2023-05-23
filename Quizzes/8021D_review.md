<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XKHR6PXZ9V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XKHR6PXZ9V');
</script>

## Introduction
9th Dec 2016

Some questions to tickle you on STP, **click the text to reveal the  answers!**

## STP Question
**Given the topology below that is running 802.1D with all settings as default, please tell me:**

<details>
  <summary>1a: What switch will be the Spanning-tree root bridge
</summary>
SW2
</details>
<details>
  <summary>1b: Why will this be the root bridge?
</summary>
It has the lowest MAC address, when all priories tie, this is the tiebreaker
</details>
<details>
  <summary>2a: What will be the BridgeID of all the BPDU's generated for VLAN 100?
</summary>
32868
</details>
<details>
  <summary>2b: What makes up this BridgeID value?
</summary>
The BridgeID is the Priority+VLANID, where the default priority is 32768
</details>
<details>
  <summary>3a: What ports on SW2 will be in the forwarding state?
</summary>
All of them
</details>
<details>
  <summary>3b: What will the forwarding port roles be?
</summary>
all root bridge downstream ports are designated forwarding ports
</details>
<details>
  <summary>4a: What port on SW4 will be the root port
</summary>
Port 1
</details>
<details>
  <summary>4b: Why will this be the root port?
</summary>
Root port is the one with the lowest cost to reach the root bridge, is there is a tie then it’s the lowest received BPDU, if there is still a tie then it’s the lowest received port priority, if there is still a tie it’s the lowest local port ID (where port 1 = 1, 2  = 2, and so on). Therefore the tie breaker here is the local port ID
</details>
<details>
  <summary>5a: On Switch 4, which ports will be designated ports?
</summary>
(0, 3 & 4)
</details>
<details>
  <summary>5b: Why will these be designated?
</summary>
Designated Ports are calculated after Root Ports, of the two sides of the link they are calculated from the viewpoint of being on the link itself. Lets look at the SW1-Sw4 link. Here it’s a cost of 10 to reach the root via Sw1 or Sw4, therefore we look at the tiebreaker methods described in Q4a, the first item looks at the lowest BPDU where in this case SW4 has a lower one based on the MAC. Therefore SW4’s Port 0 is the DP & SW1’s Port 1 is the Alt blocked port
</details>
<details>
  <summary>6a: What ports will be blocked in the topology?
</summary>
SW1’s port 1, SW4’s Port 2 & SW3’s ports 1 & 2
</details>
<details>
  <summary>6b: Why are these blocked?
</summary>
All opposite sides to Designated ports that are not Root facing Ports are set to Alternate Blocked ports, this is to stop loops
</details>

<br>

![](images/2023-01-18-14-06-44.png)



How did you do?