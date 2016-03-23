# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 20:02:51 2015

@author: daphne
"""
import instances as inst

NB_INSTANCES_PER_FILE = 10

"""
Questions 1-2
Resolution de l'exemple donné sur le poly et stocké dans grille1.txt
"""
print "--------------RESOLUTION Grille1.txt--------------"
probs = inst.read_file("grille1.txt")
inst.write_SolutionFile("grille1.txt",probs)


print
"""
Question 3
"""

print "--------------RESOLUTION Question C--------------"
#inst.questionC(NB_INSTANCES_PER_FILE)

print
"""
Question 3

"""
print "--------------RESOLUTION Question D--------------"
#inst.questionD(NB_INSTANCES_PER_FILE)

print