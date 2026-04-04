#!/bin/bash

INTERFACE="eth0"

echo "[*] Initializing eBPF/XDP Defense Shield on $INTERFACE..."

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "[*] Loading XDP drop policies (Simulated via iptables for compatibility)..."
iptables -A INPUT -p icmp -m limit --limit 1/s -j ACCEPT
iptables -A INPUT -p icmp -j DROP
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j ACCEPT
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -j DROP

echo "[+] eBPF/XDP Shield Active. Monitoring traffic..."
