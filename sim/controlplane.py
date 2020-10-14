#!/usr/bin/python


# P4 Firewall Simulator
# Pravein, 2020

#import gurobipy
#from gurobipy import GRB
from scapy.all import *
import re, sys
import logging
import os.path
import socket
import time
import pickle, pprint
import subprocess
import json

class controlplane:
    def __init__(self):
        self.controlplaneRules = {}
        self.controlplaneHit   = 0
        self.controlplaneRulesHit = {}
        self.controlplaneInternalBytes = {}
        self.controlplaneExternalBytes = {}
        self.controlplaneBytes = 0
    def printState (self):
        print "Total packets in "

    def internalPacketIn (self, flowid, pktsize):
        if flowid not in self.controlplaneRules:
            self.controlplaneRules[flowid] = 1
        else :
            self.controlplaneRules[flowid] +=1      
        self.controlplaneHit   += 1
        self.controlplaneInternalBytes[flowid] += pktsize  
        self.controlplaneBytes += pktsize
        return True
        
    def externalPacketIn (self, flowid, pktsize):
        if flowid not in self.controlplaneRules:
            return False
        else:
            self.controlplaneRulesHit[flowid] += 1 
            self.controlplaneHit += 1
            self.controlplaneExternalBytes[flowid] += pktsize
            self.controlplaneBytes += pktsize
            return True