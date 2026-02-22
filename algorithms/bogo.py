import time
import random

class bogo:
    type = 'bogo'
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

            self.swaps += len(self.list)
            random.shuffle(self.list)

            sortedCount = 0
            for i in range(len(self.list)-1):
                if self.list[i] < self.list[i+1]:
                    sortedCount += 1
            
            if sortedCount >= len(self.list)-1:
                self.finished = True
            
            self.time += (time.perf_counter_ns() - start)
