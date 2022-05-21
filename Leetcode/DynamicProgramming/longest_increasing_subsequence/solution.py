from typing import List


def LIS(A: List) -> int:
    L = [1] * len(A)
    for i in range(1, len(L)):
        sub_problems = [L[k] for k in range(i) if A[k] < A[i]]
        L[i] = 1 + max(sub_problems, default=0)
    return max(L, default=0)
