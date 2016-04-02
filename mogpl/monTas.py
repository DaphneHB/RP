# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 01:43:29 2015

@author: daphne
"""

import heapq

class MyHeap:    
    
    def __init__(self):
        self.heap = []
    
    def push(self, node):
        heapq.heappush(self.heap, (node.cout, node))
        
    def pop(self):
        # on retourne le noeud correspondant au cout minimum
        x,n = heapq.heappop(self.heap)
        return n
        
    def isEmpty(self):
        return len(self.heap)==0
    
    def __str__(self):
        string = ""
        for c,n in self.heap:
            string += "Noeud : {} de cout {}\n".format(n.coordonnees, c)
        return string
             