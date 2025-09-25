import bisect

class Solution(object):
    def lengthOfLIS(self, nums):
        sub = []
        for x in nums:
            i = bisect.bisect_left(sub, x)
            if i == len(sub):
                sub.append(x)
            else:
                sub[i] = x
        return len(sub)

if __name__ == "__main__":
    solution = Solution()
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print("Length of LIS:", solution.lengthOfLIS(nums))