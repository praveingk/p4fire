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

class p4Switch:
    def __init__(self, dataplaneSize):
        self.dataplaneRules = {}
        self.dataplaneHit   = 0
        self.dataplaneRulesHit = {}
        self.dataplaneSize = dataplaneSize
        self.controlplaneRules = {}
        self.controlplaneHit   = 0
        self.controlplaneRulesHit = {}
        self.internal = {}
        self.external = {}
        self.dropCounter = 0
        self.packetCounter = 0

    def classifyIP (self, packet):
        try :
            src = packet[IP].src
            dst = packet[IP].dst
            assignedSrc = False
            assignedDst = False

            if src not in self.internal and dst not in self.external:
                if src not in self.external and dst not in self.internal:
                    self.internal[src] = 1
                    self.external[dst] = 1
                assignedSrc = True
                assignedDst = True
            else : #src is in internal, then dst must be external
                self.external[dst] = 1
                self.internal[dst] = 1
                assignedDst = True  
                assignedSrc = True

            if assignedSrc is False:
                if src not in self.external:
                    self.external[src] = 1
                if dst not in self.internal:
                    self.internal[dst] = 1
                assignedSrc = True
                assignedDst = True
        except IndexError:
            return
        #print str(assignedSrc) + "," + str(assignedDst)

    def dumpClassification (self):
        print str(len(self.internal)) +", "+ str(len(self.external))

    def printCounters (self):
        print "Total Packets = "+ str(self.packetCounter)
        print "Total Dropped = "+ str(self.dropCounter)
        for item in self.dataplaneRules:
            print str(item) +" - "+ str(self.dataplaneRules[item])
        print str(self.dataplaneSize)

    def printSwitchStatus (self):
        print "Total Rules in dataplane : "+ str(len(self.dataplaneRules))
        print "Total external packets served in dataplane : "+ str(self.dataplaneHit)
        print "Total Rules in controlplane : "+ str(len(self.controlplaneRules))
        print "Total external packets served in controlplane : "+ str(self.controlplaneHit)
        
    def getFlowId (self, packet):
        try:
            flowid = 0
            protocol = packet[IP].proto
            if packet[IP].src in self.internal:
                if protocol == 0x06:
                    #print packet[IP].src + ", " + packet[IP].dst + ", " + str(packet[IP].proto) + ", " + str(packet[TCP].sport) + str(packet[TCP].dport)
                    flowid = (packet[IP].src, packet[IP].dst, packet[IP].proto, packet[TCP].sport, packet[TCP].dport)
                elif protocol == 0x11:
                    flowid = (packet[IP].src, packet[IP].dst, packet[IP].proto, packet[UDP].sport, packet[UDP].dport)
                else:
                    flowid = (packet[IP].src, packet[IP].dst, packet[IP].proto)
                #print "Internal " + str(flowid) + " ->   " + str(hash(flowid))
            elif packet[IP].src in self.external:
                if protocol == 0x06:
                    #print packet[IP].src + ", " + packet[IP].dst + ", " + str(packet[IP].proto) + ", " + str(packet[TCP].sport) + str(packet[TCP].dport)
                    flowid = (packet[IP].dst, packet[IP].src, packet[IP].proto, packet[TCP].dport, packet[TCP].sport)
                elif protocol == 0x11:
                    flowid = (packet[IP].dst, packet[IP].src, packet[IP].proto, packet[UDP].dport, packet[UDP].sport)
                else:
                    flowid = (packet[IP].dst, packet[IP].src, packet[IP].proto)
                #print "External " + str(flowid) + " ->   " + str(hash(flowid))                
            else:
                #print "Not in either.. Dropping"
                flowid = (packet[IP].src, packet[IP].dst, packet[IP].proto)
                self.dropCounter += 1
                print str(flowid)
            return hash(flowid)
        except IndexError:
            return
            
    def packetIn(self, packet):
        try :
            flowid = self.getFlowId(packet) 
            if packet[IP].src in self.internal:
                if flowid not in self.dataplaneRules:
                    self.dataplaneRules[flowid] = 1
                    if self.dataplaneSize == 0:
                        self.controlplaneRules[flowid] = 1
                    self.dataplaneSize -=1
                    #print str(flowid) + " - " + str(self.dataplaneRules[flowid])
                else :
                    self.dataplaneRules[flowid] +=1
            

            self.packetCounter += 1
        except IndexError:
            return

