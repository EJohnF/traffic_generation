#!/bin/bash

port=$2
ip=$1
sudo nmap -sA $ip -p $port
sudo nmap -b $ip -p $port
sudo nmap -sT $ip -p $port
sudo nmap -sF $ip -p $port
sudo nmap -sI $ip -p $port
sudo nmap -sM $ip -p $port
sudo nmap -sN $ip -p $port
sudo nmap -sS $ip -p $port
sudo nmap -sW $ip -p $port
sudo nmap -sX $ip -p $port
