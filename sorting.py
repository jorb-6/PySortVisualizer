import random
import math
import time

def randomList(size):
    list = []
    for i in range(size):
        list.append(i+1)
    random.shuffle(list)
    return list

def isSorted(list):
    for i in range(len(list)-1):
        if list[i] > list[i+1]:
            return False
    return True
