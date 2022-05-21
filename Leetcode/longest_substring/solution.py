class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        ans = start = 0
        last_seen = {}
        for end, c in enumerate(s):
            if c in last_seen:
                start = max(last_seen[c], start)
            ans = max(ans, end - start + 1)
            last_seen[c] = end + 1

        return ans