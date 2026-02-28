import time
import random

class bogo:
    type = 'bogo: bogo'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = -1
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            self.swaps += len(self.list)
            random.shuffle(self.list)

            sortedCount = 0
            for i in range(len(self.list)-1):
                if self.list[i] < self.list[i+1]:
                    sortedCount += 1
            
            if sortedCount >= len(self.list)-1:
                self.finished = True
            
            self.time += (time.perf_counter_ns() - start)

# yes, this is faked, but why the hell would i actually optimize bogo sort?
class optimized_bogo:
    type = 'bogo: optimized bogo'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 0
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            suffix = self.list[self.pointer:]
            self.swaps += len(suffix)
            random.shuffle(suffix)
            self.list[self.pointer:] = suffix

            while self.list[self.pointer] == self.pointer+1: # assumes 1..n list, no breaks between numbers
                self.pointer += 1
                if self.pointer >= len(self.list):
                    self.finished = True
                    return
            
            self.time += (time.perf_counter_ns() - start)
