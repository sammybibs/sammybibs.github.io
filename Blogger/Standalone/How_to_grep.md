# Contents
  - [Introduction](#introduction-)
  - [IOS regexp](#ios-regexp-)
  - [Summary](#summary-)
  - [Further reading](#further-reading-)

## Introduction <a name="introduction"></a>
I learn regular expressions, I forget regular expressions. I learn regular expressions, I forget regular expressions. Sound familiar?

Some of this stuff sticks for a while, but the devil is in the details & if like me you rarely use them in your day to day, well the information just evaporates out of your ears.

Typically if you are a non Linux/Unix fellow, then your regexp usage would come from BGP. If you are not a regular user of BGP then how else can one make use of these tools?

## IOS regexp <a name="ios-regexp"></a>
There is another way you can get more out of regular expressions & use them in your day to day therefore helping you to commit this info to long term memory. What i am talking about is the grep functionality of Cisco IOS (tested in IOS & XE).

<br>

```
R10#conf t
R10(config)#shell processing full
```

This allows us to call on the grep functionality to search within output, lets use this to look for an IP address within our configuration:

```
R10#show run | grep [0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*
 ip address 150.1.10.10 255.255.255.255
 ip address 172.16.5.6 255.255.255.0
 ip igmp join-group 225.1.2.3
 ip address 155.1.10.10 255.255.255.0
```

From this we can see the grep functionality has worked, lets breakdown what exactly we did to glean this information:
1. First off we have set a criteria of a range from 0-9 within the square brackets [0-9], here we are saying any value from 0-9. 
2. Next up is the *, this special character matches zero or more occurrences of the preceding character. Therefore we would match nothing ' ', one single character '1' or '3' & also multiple numerical characters '123' or '222'.
3. The next character's, the double \\ tells grep that the dot '.' that follows the \\ is to interpreted as a literal dot, not a special character (the dot would otherwise mean  match any single character including a blank space)

The above pattern is repeated 4 times, to look for four sets of numerical values that are separated by a dot. Which is what makes up an IPv4 address.

Lets quickly talk about why we need the double backslash before we move on, first lets look at what the CLI interprets these as by way of echo:

```
R10#echo \

R10#echo \\
\
R10#echo '\'
\
R10#echo '\\'
\\
R10#echo \.
.
R10#echo \\.
\.
```

As you can see if we exclude single quotations ' ' then the \ has special meaning to the parser & is not displayed. What is interesting & I don't yet know the answer is, why do i need a double \\ to make the dot appear in its true form, when the echo above shows that only a single slash is needed to parse the following data correctly. I would expect my IPv4 regexp to interpret the second slash as literal as per the final echo output.

What I understand is that the \ is also a shell quoting character & hard to use as an escape character, thereby double \\ may be needed for grep but not for the echo command.

To avoid the double \\, you can just put your expression inside of single quotes ' ' & use a single slash \

```
R10#show run | grep '[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*'
ip domain name 1a.23.45.6
 ip address 150.1.10.10 255.255.255.255
 ip address 192.168.0.1 255.255.255.0
 ip address 172.16.5.6 255.255.255.0
 ip igmp join-group 225.1.2.3
 ip address 155.1.10.10 255.255.255.0
 ip address 155.1.108.10 255.255.255.0
```

You may noticed I have added a domain name that looks somewhat like an IP address. However we do not want to match on this, but the reason we are is due to the * in the search, whereby the * matches zero or more occurrences of the preceding character. In this case the domain name is matched by the zero value, as the character before the first dot '.' can be numerical or nothing (zero).

To fix this we substitute the * with a +, where the + sign indicates that we much match one or more of the preceding values. Meaning there must be a numerical value before the dot '.'.

```
R10#show run | grep '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
 ip address 150.1.10.10 255.255.255.255
 ip address 192.168.0.1 255.255.255.0
 ip address 172.16.5.6 255.255.255.0
 ip igmp join-group 225.1.2.3
 ip address 155.1.10.10 255.255.255.0
 ip address 155.1.108.10 255.255.255.0
```

However if we now modify the domain name to 'bib127.0.0.1', we should match it again as the character preceding the first dot '.' is numerical.

```
R10#show run | grep '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
ip domain name bib127.0.0.1
 ip address 150.1.10.10 255.255.255.255
 ip address 192.168.0.1 255.255.255.0
 ip address 172.16.5.6 255.255.255.0
 ip igmp join-group 225.1.2.3
 ip address 155.1.10.10 255.255.255.0
 ip address 155.1.108.10 255.255.255.0
```

We know that in our example there is a leading white space, therefore we can add this into out filter to remove the unwanted results, here are both methods:

```
R10#show run | grep ' [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
R10#show run | grep \ [0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+
 ip address 150.1.10.10 255.255.255.255
 ip address 192.168.0.1 255.255.255.0
 ip address 172.16.5.6 255.255.255.0
 ip igmp join-group 225.1.2.3
 ip address 155.1.10.10 255.255.255.0
 ip address 155.1.108.10 255.255.255.0
```

We do have the _ underscore to match on white space, but testing has shown this not to work with grep, however it does work with regexp for searching the BGP tables.

As you can see the grep feature can be used as part of your day to day, try swapping out the 'include' & 'section' searches & use grep instead, your future self will thank you for it!

## Summary <a name="summary"></a>
Now finally by way of example, here are some regexp's I have taken from my notes and the results they would yield:

* ^100:1_ Match 100:1 at the start of the line
* 200:3$ Match 200:3 at the end of the line
* 300:[5-9]_ Match a range from 300:5 to 300:9 the _ signifies the end so only 1 digit allowed after the :
* 400:1.*_ Matches 400:1XXXX where X is anything as the . means any character & the * means the previous match the previous charterer 0 or more times.
* 400:1.+_ is as previous, but wont match 400:1 as the + means 1 or more times, so a second character is needed.
* 500:([0-9]2)+_ inside the ( ) is treated as one expression where the + means this expression must be there 1 or more times, so 500:X2 & 500:X2X2X2 all match.
* 600:1_ | 600:2_ is using a | alternate, which looks for either of the patterns
* 600:(12)|(22) uses the | OR to look for 600:12 or 600:22

## Further reading <a name="further-reading"></a>
[Cisco Regexp;(http://www.cisco.com/c/en/us/td/docs/ios/12_2/termserv/configuration/guide/ftersv_c/tcfaapre.html#wp1023226)
[Cisco Shell Processing](http://www.cisco.com/c/en/us/td/docs/ios/netmgmt/configuration/guide/Convert/IOS_Shell/nm_ios_shell.html)

