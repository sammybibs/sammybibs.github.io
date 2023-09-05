# Contents
- [CCNP SEC Blueprint tracker](#ccnp-sec-blueprint-tracker-)
- [Exam Topics: Section:](#exam-topics:-section:-)
  - [1.0 Security Concepts](#1.0-security-concepts-)
  - [2.0 Network Security](#2.0-network-security-)
  - [3.0 Securing the Cloud](#3.0-securing-the-cloud-)
  - [4.0 Content Security](#4.0-content-security-)
  - [6.0 Secure Network Access, Visibility, and Enforcement](#6.0-secure-network-access,-visibility,-and-enforcement-)

<script>
for i in datas.split("\n"):
  print("| "+i+" |  Y |")
</script>



# Study resources
https://ondemandelearning.cisco.com/cisco-ems/scor10/sections/1/pages/1
https://u.cisco.com/search?query=350-701
https://learning.oreilly.com/library/view/ccnp-and-ccie/9780135971802/


# CCNP SEC Blueprint tracker <a name="ccnp-sec-blueprint-tracker"></a>
Last assessed == NEVER

# Exam Topics: Section: <a name="exam-topics:-section:"></a>


## 1.0 Security Concepts <a name="1.0-security-concepts"></a>


| Topic         | Need to study?|
| ------------- |:-------------:|
| 1.1 Explain common threats against on-premises, hybrid, and cloud environments |  Y |
| 1.1.a On-premises: viruses, trojans, DoS/DDoS attacks, phishing, rootkits, man-in-themiddle attacks, SQL injection, cross-site scripting, malware |  Y |
| 1.1.b Cloud: data breaches, insecure APIs, DoS/DDoS, compromised credentials |  Y |
| 1.2 Compare common security vulnerabilities such as software bugs, weak and/or hardcoded passwords, OWASP top ten, missing encryption ciphers, buffer overflow, path traversal, cross-site scripting/forgery |  Y |
| 1.3 Describe functions of the cryptography components such as hashing, encryption, PKI, SSL, IPsec, NAT-T IPv4 for IPsec, preshared key, and certificate-based authorization |  Y |
| 1.4 Compare site-to-site and remote access VPN deployment types and components such as virtual tunnel interfaces, standards-based IPsec, DMVPN, FlexVPN, and Cisco Secure Client including high availability considerations |  Y |
| 1.5 Describe security intelligence authoring, sharing, and consumption |  Y |
| 1.6 Describe the controls used to protect against phishing and social engineering attacks |  Y |
| 1.7 Explain North Bound and South Bound APIs in the SDN architecture |  Y |
| 1.8 Explain Cisco DNA Center APIs for network provisioning, optimization, monitoring, and troubleshooting |  Y |
| 1.9 Interpret basic Python scripts used to call Cisco Security appliances APIs |  Y |

<br>

## 2.0 Network Security <a name="2.0-network-security"></a>

| Topic         | Need to study?|
| ------------- |:-------------:|
| 2.1 Compare network security solutions that provide intrusion prevention and firewall capabilities |  Y |
| 2.2 Describe deployment models of network security solutions and architectures that provide intrusion prevention and firewall capabilities |  Y |
| 2.3 Describe the components, capabilities, and benefits of NetFlow and Flexible NetFlow records |  Y |
| 2.4 Configure and verify network infrastructure security methods |  Y |
| 2.4.a Layer 2 methods (network segmentation using VLANs; Layer 2 and port security; DHCP snooping; Dynamic ARP inspection; storm control; PVLANs to segregate network traffic; and defenses against MAC, ARP, VLAN hopping, STP, and DHCP rogue attacks) |  Y |
| 2.4.b Device hardening of network infrastructure security devices (control plane, data plane, and management plane) |  Y |
| 2.5 Implement segmentation, access control policies, AVC, URL filtering, malware protection, and intrusion policies |  Y |
| 2.6 Implement management options for network security solutions (single vs. multidevice manager, in-band vs. out-of-band, cloud vs. on-premises) |  Y |
| 2.7 Configure AAA for device and network access such as TACACS+ and RADIUS |  Y |
| 2.8 Configure secure network management of perimeter security and infrastructure devices such as SNMPv3, NetConf, RestConf, APIs, secure syslog, and NTP with authentication |  Y |
| 2.9 Configure and verify site-to-site and remote access VPN |  Y |
| 2.9.a Site-to-site VPN using Cisco routers and IOS |  Y |
| 2.9.b Remote access VPN using Cisco AnyConnect Secure Mobility client |  Y |
| 2.9.c Debug commands to view IPsec tunnel establishment and troubleshooting |  Y |

<br>

## 3.0 Securing the Cloud <a name="3.0-securing-the-cloud"></a>

| Topic         | Need to study?|
| ------------- |:-------------:|
| 3.1 Identify security solutions for cloud environments |  Y |
| 3.1.a Public, private, hybrid, and community clouds |  Y |
| 3.1.b Cloud service models: SaaS, PaaS, IaaS (NIST 800-145) |  Y |
| 3.2 Compare security responsibility for the different cloud service models |  Y |
| 3.2.a Patch management in the cloud |  Y |
| 3.2.b Security assessment in the cloud |  Y |
| 3.3 Describe the concept of DevSecOps (CI/CD pipeline, container orchestration, and secure software development) |  Y |
| 3.4 Implement application and data security in cloud environments |  Y |
| 3.5 Identify security capabilities, deployment models, and policy management to secure the cloud |  Y |
| 3.6 Configure cloud logging and monitoring methodologies |  Y |
| 3.7 Describe application and workload security concepts |  Y |

<br>

## 4.0 Content Security <a name="4.0-content-security"></a>

| Topic         | Need to study?|
| ------------- |:-------------:|
| 4.1 Implement traffic redirection and capture methods for web proxy |  Y |
| 4.2 Describe web proxy identity and authentication including transparent user identification |  Y |
| 4.3 Compare the components, capabilities, and benefits of on-premises, hybrid, and cloudbased email and web solutions (Cisco Secure Email Gateway, Cisco Secure Email Cloud Gateway, and Cisco Secure Web Appliance) |  Y |
| 4.4 Configure and verify web and email security deployment methods to protect onpremises, hybrid, and remote users |  Y |
| 4.5 Configure and verify email security features such as SPAM filtering, antimalware filtering, DLP, blocklisting, and email encryption |  Y |
| 4.6 Configure and verify Cisco Umbrella Secure Internet Gateway and web security features such as blocklisting, URL filtering, malware scanning, URL categorization, web application filtering, and TLS decryption |  Y |
| 4.7 Describe the components, capabilities, and benefits of Cisco Umbrella |  Y |
| 4.8 Configure and verify web security controls on Cisco Umbrella (identities, URL content settings, destination lists, and reporting) |  Y |

<br>

 ## 5.0 Endpoint Protection and Detection
| Topic         | Need to study?|
| ------------- |:-------------:|
| 5.1 Compare Endpoint Protection Platforms (EPP) and Endpoint Detection & Response (EDR) solutions |  Y |
| 5.2 Configure endpoint antimalware protection using Cisco Secure Endpoint |  Y |
| 5.3 Configure and verify outbreak control and quarantines to limit infection |  Y |
| 5.4 Describe justifications for endpoint-based security |  Y |
| 5.5 Describe the value of endpoint device management and asset inventory systems such as MDM |  Y |
| 5.6 Describe the uses and importance of a multifactor authentication (MFA) strategy |  Y |
| 5.7 Describe endpoint posture assessment solutions to ensure endpoint security |  Y |
| 5.8 Explain the importance of an endpoint patching strategy |  Y |

<br>

##  6.0 Secure Network Access, Visibility, and Enforcement <a name="6.0-secure-network-access,-visibility,-and-enforcement"></a>
| Topic         | Need to study?|
| ------------- |:-------------:|
| 6.1 Describe identity management and secure network access concepts such as guest services, profiling, posture assessment and BYOD |  Y |
| 6.2 Configure and verify network access control mechanisms such as 802.1X, MAB, WebAuth |  Y |
| 6.3 Describe network access with CoA |  Y |
| 6.4 Describe the benefits of device compliance and application control |  Y |
| 6.5 Explain exfiltration techniques (DNS tunneling, HTTPS, email, FTP/SSH/SCP/SFTP, ICMP, Messenger, IRC, NTP) |  Y |
| 6.6 Describe the benefits of network telemetry |  Y |
| 6.7 Describe the components, capabilities, and benefits of these security products and solutions |  Y |
| 6.7.a Cisco Secure Network Analytics |  Y |
| 6.7.b Cisco Secure Cloud Analytics |  Y |
| 6.7.c Cisco pxGrid |  Y |
| 6.7.d Cisco Umbrella Investigate |  Y |
| 6.7.e Cisco Cognitive Intelligence |  Y |
| 6.7.f Cisco Encrypted Traffic Analytics |  Y |
| 6.7.g Cisco Secure Client Network Visibility Module (NVM) |  Y |

