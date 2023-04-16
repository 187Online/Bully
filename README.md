
# Bully 2.0 released



:gift_heart: Every star you give me is a motivation, please give a star if you like it.

Bully Python DoS Attack Tool 
* UDP Storm 
* SYN Flood
* ICMP Bomb
* ICMP Flood 
* Sockstress 
* Slowloris
* Get 
* PPS
* Post 
* XMLRPC 
* KILL
* CUSTOM
* SSL (experimental)

## Bully Update Notes 
 Bully is now more powerful and faster than older versions.
 
 The Bully Python DoS tool has been updated! The new version is now easier to use. Here are the update notes:
 
 Bully 1.3 Updates =>
* The Smurf attack feature has been removed because it was ineffective.
* The SSL DoS (handshake spam) feature has been updated.
* The HTTP packet feature has been updated.
* The overall structure has been converted to object-oriented programming.
* The XML-RPC feature has been added.
* CLI reconfigured.
* Argparse readded.
* Multiprocessing added
* High-power attack using all processor cores.
* KILL method added.
* Illegal IP address bug fixed .
* Sockstress and SYN flood bugs fixed .
* SSL Handshake spam bug fixed and reconfigured.

Bully 2.0 Update notes =>
* While loops have been removed for the use of command line interfaces, and instead, only argparse  has been introduced.
* Layer classes are defined as objects, and multiprocessing is only assigned to the worker class .
* KILL method updated more powerful and controlable than old version. 
* Outputs were made more orderly by removing unnecessary colors.
* The number of CPU cores used is now optional.
* Bully was generally optimized.
* Custom method added.
* Signal added.
* Process barrier added.
* Error outputs were made more readable and controlable.

## Legal Warning 

* This software is for educational purposes only

## Usage

Clone

```bash
  git clone https://github.com/187Online/Bully.git
```

Usage
```bash
  python Bully.py -target <url> -m <method> -s <concurrent socket> -w <concurrent workers> 
```

## Lisans

[MIT](https://choosealicense.com/licenses/mit/)

  
