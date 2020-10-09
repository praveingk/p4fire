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

class dataplane:
    def __init__(self, dataplaneSize):
        self.dataplaneRules = {}
        self.dataplaneHit   = 0
        self.dataplaneRulesHit = {}
        self.dataplaneSize = dataplaneSize    

    def internalPacketIn (self, flowid):
        if flowid not in self.dataplaneRules:
            self.dataplaneRules[flowid] = 1
            if self.dataplaneSize == 0:
                return False
            self.dataplaneSize -=1
                    #print str(flowid) + " - " + str(self.dataplaneRules[flowid])
        else :
            self.dataplaneRules[flowid] +=1        
        return True
        
    def externalPacketIn (self, flowid):
        if flowid not in self.dataplaneRules:
            return False
        else:
            self.dataplaneRulesHit[flowid] += 1 
            self.dataplaneHit += 1
            return True
