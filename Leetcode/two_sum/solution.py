class Solution:

    def twoSum(self, nums, target):

        errors = {}
        for i, num in enumerate(nums):
            diff = target - num
            if num in errors:
                return [errors.get(num), i]
            errors[diff] = i
        return -1