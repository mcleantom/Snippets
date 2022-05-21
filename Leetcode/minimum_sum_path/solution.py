import sys

class Solution:

    def minPathSum(self, grid):
        M = len(grid)
        N = len(grid[0])
        dp = [0] + [sys.maxsize] * (N-1)
        for i in range(M):
            dp[0] = dp[0] + grid[i][0]
            for j in range(1, N):
                dp[j] = min(dp[j-1], dp[j]) + grid[i][j]
        return dp[-1]