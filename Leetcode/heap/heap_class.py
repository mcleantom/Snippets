from typing import Generic, TypeVar, List
from heapq import heapify
T = TypeVar("T")


class Heap(Generic[T]):

    def __init__(self):
        self.is_max_heap = False
        self.elements: List[T] = []
        self.length = 0

    def _swap(self, i, j):
        t: T = self.elements[i]
        self.elements[i] = self.elements[j]
        self.elements[j] = t

    def _update_length(self):
        self.length = len(self.elements)

    def compare(self, a: T, b: T):
        if a > b:
            return 1
        if a < b:
            return -1
        return 0

    def _get_max_index(self, i, j, k):
        if (
            (self.compare(self.elements[i], self.elements[j]) >= 0) and
            (self.compare(self.elements[i], self.elements[k]) >=0)
        ):
            return i
        elif (
            (self.compare(self.elements[j], self.elements[i]) >= 0) and
            (self.compare(self.elements[j], self.elements[k]) >=0)
        ):
            return j
        return k

    def _get_min_index(self, i, j, k):
        if (
            (self.compare(self.elements[i], self.elements[j]) <= 0) and
            (self.compare(self.elements[i], self.elements[k]) <=0)
        ):
            return i
        elif (
            (self.compare(self.elements[j], self.elements[i]) <= 0) and
            (self.compare(self.elements[j], self.elements[k]) <= 0)
        ):
            return j
        return k

    def _adjust_up_down(self, i):
        if (i*2 < self.length and i*2+1 < self.length):
            if self.is_max_heap:
                k = self._get_max_index(i, i*2, i*2+1)
            else:
                k = self._get_min_index(i, i*2, i*2+1)
            if (k==1):
                return
            else:
                self._swap(i, k)
                self._adjust_up_down(k)
                return
        elif (i*2 < self.length):
            if (
                ((self.compare(self.elements[i], self.elements[i*2])<0) and self.is_max_heap) or
                ((self.compare(self.elements[i], self.elements[i*2])>0 and not self.is_max_heap))
            ):
                self._swap(i, i*2)
                self._adjust_up_down(i*2)