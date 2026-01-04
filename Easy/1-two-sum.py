# Topics: Arrays, Hash Table, Two Pointers
# Problem: 1. Two Sum
# Difficulty: Easy

class Solution:
    def twoSum(self, nums, target):
        """
        Find two numbers that add up to target.
        
        Args:
            nums: List of integers
            target: Target sum
            
        Returns:
            List of indices [i, j] where nums[i] + nums[j] == target
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []


# Example usage:
# sol = Solution()
# print(sol.twoSum([2, 7, 11, 15], 9))  # Output: [0, 1]
