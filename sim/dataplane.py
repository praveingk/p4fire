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

    def packetIn(self, packet, portType):
        