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

    def internalPacketIn (self, flowid):
        if flowid not in self.controlplaneRules:
            self.controlplaneRules[flowid] = 1
        else :
            self.controlplaneRules[flowid] +=1        
        return True
        
    def externalPacketIn (self, flowid):
        if flowid not in self.controlplaneRules:
            return False
        else:
            self.controlplaneRulesHit[flowid] += 1 
            self.controlplaneHit += 1
    
            return True