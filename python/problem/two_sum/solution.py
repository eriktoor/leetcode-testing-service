class Solution:
    def two_sum(self, nums, target):
        seen = {}
        
        for index, val in enumerate(nums):
            seen[val] = index
        
        for index, val in enumerate(nums):
            if target - val in seen:
                if index != seen[target-val]: return [index, seen[target-val]]