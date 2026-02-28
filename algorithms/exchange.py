import time
import math

class exchange:
    type = 'exchange: exchange'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 0
        self.pointer1 = 0
        self.mode = 1
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return
            
            if self.pointer >= len(self.list)-2:
                self.finished = True
                return

            if self.mode == 0:
                self.pointer += 1
                self.pointer1 = self.pointer + 1
                self.mode = 1
            
            elif self.mode == 1:
                self.comparisons += 1
                if self.list[self.pointer] > self.list[self.pointer1]:
                    self.swaps += 1
                    self.list[self.pointer], self.list[self.pointer1] = self.list[self.pointer1], self.list[self.pointer]
                self.pointer1 += 1
                if self.pointer1 > len(self.list)-1:
                    self.pointer1 = 0
                    self.mode = 0
            
            self.time += time.perf_counter_ns() - start

class gnome:
    type = 'exchange: gnome'
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
            
            if self.pointer >= len(self.list):
                self.finished = True
                return

            if self.list[self.pointer] >= self.list[self.pointer - 1]:
                self.pointer += 1
            else:
                self.list[self.pointer], self.list[self.pointer - 1] = self.list[self.pointer - 1], self.list[self.pointer]
                self.pointer -= 1
                if self.pointer == 0:
                    self.pointer = 1
            
            self.time += time.perf_counter_ns() - start

class bubble:
    type = 'exchange: bubble'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 0
        self.fullLoops = 0
        self.swapped = False
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            self.comparisons += 1
            if self.list[self.pointer] > self.list[self.pointer+1]:
                b = self.list[self.pointer+1]
                self.list[self.pointer+1] = self.list[self.pointer]
                self.list[self.pointer] = b
                self.swaps += 1
                self.swapped = True
            self.pointer += 1
            if self.pointer > len(self.list) - self.fullLoops - 2:
                self.pointer = 0
                self.fullLoops += 1
                if self.swapped:
                    self.swapped = False
                else:
                    self.finished = True
            
            self.time += (time.perf_counter_ns() - start)

class cocktail_shaker:
    type = 'exchange: cocktail shaker'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 0
        self.pointer1 = 0
        self.pointer2 = len(self.list)-1
        self.mode = 0   # 0 = reset swapped, 1 = forward pass, 2 = check if sorted, 3 = backwards pass, 4 = increment start
        self.swapped = False
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            if self.mode == 0:
                self.swapped = False
                self.pointer = self.pointer1
                self.mode = 1
            
            elif self.mode == 1:
                if self.pointer >= self.pointer2:
                    self.mode = 2
                else:
                    self.comparisons += 1
                    if self.list[self.pointer] > self.list[self.pointer + 1]:
                        self.swaps += 1
                        self.list[self.pointer], self.list[self.pointer + 1] = self.list[self.pointer + 1], self.list[self.pointer]
                        self.swapped = True
                    self.pointer += 1
            
            elif self.mode == 2:
                if not self.swapped:
                    self.finished = True
                    break
                self.pointer2 -= 1
                self.swapped = False
                self.pointer = self.pointer2-1
                self.mode = 3
            
            elif self.mode == 3:
                if self.pointer <= self.pointer1:
                    self.mode = 4
                else:
                    self.comparisons += 1
                    if self.list[self.pointer] > self.list[self.pointer + 1]:
                        self.swaps += 1
                        self.list[self.pointer], self.list[self.pointer + 1] = self.list[self.pointer + 1], self.list[self.pointer]
                        self.swapped = True
                    self.pointer -= 1
            
            elif self.mode == 4:
                self.mode = 1
                self.pointer1 += 1
            
            self.time += (time.perf_counter_ns() - start)

class odd_even:
    type = 'exchange: odd-even'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 1
        self.swapped = False
        self.mode = 0
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            if self.mode == 0:
                self.comparisons += 1
                if self.list[self.pointer] > self.list[self.pointer + 1]:
                    self.swaps += 1
                    self.swapped = True
                    self.list[self.pointer], self.list[self.pointer + 1] = self.list[self.pointer + 1], self.list[self.pointer]
                self.pointer += 2
                if self.pointer >= len(self.list) - 1:
                    self.mode = 1
                    self.pointer = 0
                    if self.swapped:
                        self.swapped = False
                    else:
                        self.finished = True
                        return
            
            elif self.mode == 1:
                self.comparisons += 1
                if self.list[self.pointer] > self.list[self.pointer + 1]:
                    self.swaps += 1
                    self.swapped = True
                    self.list[self.pointer], self.list[self.pointer + 1] = self.list[self.pointer + 1], self.list[self.pointer]
                self.pointer += 2
                if self.pointer >= len(self.list) - 1:
                    self.mode = 0
                    self.pointer = 1
                    if self.swapped:
                        self.swapped = False
                    else:
                        self.finished = True
                        return
            
            self.time += (time.perf_counter_ns() - start)

class comb:
    type = 'exchange: comb'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int], shrink: float = 1.3):
        self.list = nums
        self.swapped = False
        self.pointer = 0
        self.pointer1 = 0
        self.gap = len(nums)
        self.shrink = shrink
        self.mode = 0       # 0 = shrink, 1 = sort
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return
            
            if self.mode == 0:
                self.gap = max(math.floor(self.gap / self.shrink), 1)
                self.mode = 1
            
            elif self.mode == 1:
                if self.pointer < len(self.list) - self.gap:
                    i = self.pointer
                    self.comparisons += 1
                    if self.list[i] > self.list[i + self.gap]:
                        self.list[i], self.list[i + self.gap] = self.list[i + self.gap], self.list[i]
                        self.swapped = True
                        self.swaps += 1
                    self.pointer += 1
                else:
                    self.pointer = 0
                    self.mode = 0
                    if self.swapped:
                        self.swapped = False
                    else:
                        self.finished = True
            
            self.pointer1 = self.pointer + self.gap
            
            self.time += (time.perf_counter_ns() - start)