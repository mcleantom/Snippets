def solution(nums, target):
    start = 0
    end = len(nums)-1
    while start <= end:
        middle = int((start+end)/2)
        val = nums[middle]
        if val == target:
            return middle
        if val < target:
            start = middle+1
        else:
            end = middle-1
    return -1