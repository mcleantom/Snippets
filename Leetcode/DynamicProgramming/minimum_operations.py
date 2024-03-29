from collections import deque
from typing import List


def minimumOperations(nums: List[int], start: int, goal: int) -> int:
    seen = set()

    # If a candidate number requires the current number to be outside the range (0, 1000) to meet the goal, then filter it out.
    filtered_nums = []
    for num in nums:
        # outside range
        outside = num < 0 or num > 1000
        # requires number outside of [0, 1000] to reach goal with addition
        add_check = (goal - num < 0 or goal - num > 1000)
        # requires number outside of [0, 1000] to reach goal with subtraction
        sub_check = (goal + num < 0 or goal + num > 1000)
        # requires number outside of [0, 1000] to reach goal with xor
        xor_check = (goal ^ num > 1000 or goal ^ num < 0)

        # Perform all checks above, and also filter out 0
        if not (outside and add_check and sub_check and xor_check) and num:
            filtered_nums.append(num)
    nums = filtered_nums
    del filtered_nums

    q = deque([(start, 0)])
    while q:
        cur, steps = q.popleft()
        for num in nums:
            for cand in (cur + num, cur - num, cur ^ num):
                if cand == goal:
                    return steps + 1
                if cand not in seen and 0 <= cand <= 1000:
                    q.append((cand, steps + 1))
                    seen.add(cand)

    return -1


assert minimumOperations(nums = [2,4,12], start = 2, goal = 12) == 2
assert minimumOperations(nums = [3,5,7], start = 0, goal = -4) == 2
assert minimumOperations(nums = [2,8,16], start = 0, goal = 1) == -1