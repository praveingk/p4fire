#!/usr/bin/python


# P4 Firewall Simulator
# Pravein, 2020

import gurobipy
from gurobipy import GRB
from scapy.all import *
import re, sys
import logging
import os.path
import socket
import time
import pickle, pprint
import subprocess
import json


from p4Switch import p4Switch


pcapfile = ""
dataplaneSize = 100000

def printUsage():
    print "Usage:  p4firesim.py <pcapfile>"

def startSimTraffic (pcapfile):
    print "Loading "+ pcapfile+".."
    packets = rdpcap(pcapfile)
    print "Starting P4 Firewall"
    mySwitch = p4Switch(dataplaneSize)
    for packet in packets:
        mySwitch.classifyIP(packet)
    mySwitch.dumpClassification()
    
    for packet in packets:
        mySwitch.packetIn(packet)
    mySwitch.printCounters()


if len(sys.argv) < 2:
    printUsage()
else :
    pcapfile = str(sys.argv[1])
    startSimTraffic(pcapfile)