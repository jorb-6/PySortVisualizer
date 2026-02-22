import time
import math

class bubble:
    type = 'bubble'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.iteration = 0
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
            self.iteration += 1
            if self.pointer > len(self.list) - self.fullLoops - 2:
                self.pointer = 0
                self.fullLoops += 1
                if self.swapped:
                    self.swapped = False
                else:
                    self.finished = True
            
            self.time += (time.perf_counter_ns() - start)

class comb:
    type = 'comb'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int], shrink: float = 1.3):
        self.list = nums
        self.iteration = 0
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
            
            if self.mode == 1:
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

class insertion:
    type = 'insertion'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.iteration = 0
        self.pointer = 1
        self.pointer1 = 0
        self.key = 0
        self.mode = 0   # 0 = set key, 1 = shift, 2 = insert
    
    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            if self.mode == 0:
                if self.pointer >= len(self.list):
                    self.finished = True
                    return
                self.key = self.list[self.pointer]
                self.pointer1 = self.pointer - 1
                self.mode = 1
            
            if self.mode == 1:
                if self.pointer1 >= 0:
                    self.comparisons += 1
                    if self.list[self.pointer1] > self.key:
                        self.swaps += 1
                        self.list[self.pointer1 + 1] = self.list[self.pointer1]
                        self.pointer1 -= 1
                    else:
                        self.mode = 2
                else:
                    self.mode = 2
            
            if self.mode == 2:
                self.swaps += 1
                self.list[self.pointer1 + 1] = self.key
                self.pointer += 1
                self.mode = 0
            
            self.time += (time.perf_counter_ns() - start)

class shell:
    type = 'shell'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.gap = len(nums) // 2
        self.pointer = self.gap
        self.pointer1 = 0
        self.key = 0
        self.mode = 1   # 0 = set key, 1 = shift, 2 = insert
        self.finished = False

    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            if self.gap == 0:
                self.finished = True
                return

            if self.mode == 0:
                if self.pointer >= len(self.list):
                    self.gap //= 2
                    self.pointer = self.gap
                    if self.gap == 0:
                        self.finished = True
                        return
                else:
                    self.key = self.list[self.pointer]
                    self.pointer1 = self.pointer
                    self.mode = 1

            elif self.mode == 1:
                if self.pointer1 >= self.gap:
                    self.comparisons += 1
                    if self.list[self.pointer1 - self.gap] > self.key:
                        self.swaps += 1
                        self.list[self.pointer1] = self.list[self.pointer1 - self.gap]
                        self.pointer1 -= self.gap
                    else:
                        self.mode = 2
                else:
                    self.mode = 2

            elif self.mode == 2:
                self.swaps += 1
                self.list[self.pointer1] = self.key
                self.pointer += 1
                self.mode = 0
            
            self.time += (time.perf_counter_ns() - start)

class selection:
    type = 'selection'
    finished = False
    time = 0
    swaps = 0
    comparisons = 0

    def __init__(self, nums: list[int]):
        self.list = nums
        self.pointer = 0
        self.pointer1 = 0
        self.minNumIdx = 0
        self.mode = 1   # 0 = reset minimum, 1 = find minimum, 2 = swap
        self.finished = False

    def step(self, times: int = 1):
        for _ in range(times):
            start = time.perf_counter_ns()

            if self.finished:
                return

            if self.pointer >= len(self.list):
                self.finished = True
                return

            if self.mode == 0:
                self.minNumIdx = self.pointer
                self.pointer1 = self.pointer + 1
                self.mode = 1
            
            if self.mode == 1:
                if self.pointer1 < len(self.list):
                    self.comparisons += 1
                    if self.list[self.pointer1] < self.list[self.minNumIdx]:
                        self.minNumIdx = self.pointer1
                    self.pointer1 += 1
                else:
                    self.mode = 2
            
            if self.mode == 2:
                self.swaps += 1
                self.list[self.pointer], self.list[self.minNumIdx] = (
                    self.list[self.minNumIdx], self.list[self.pointer])
                self.pointer += 1
                self.mode = 0
            
            self.time += (time.perf_counter_ns() - start)