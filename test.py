class Solution:
    def numDecodings(self, s: str) -> int:
        possible_encodings = set(str(c) for c in range(1, 27))
        total = 0

        def dp(s, total=0):
            if len(s) == 1:
                total += int(s in possible_encodings)
            elif len(s) == 2:
                total += int(s in possible_encodings) + int(s[-1] in possible_encodings)
            else:
                if s[-1] in possible_encodings:
                    total += dp(s[:-1])
                if s[-2:] in possible_encodings:
                    total += dp(s[:-2])
            return total

        return dp(s)



solution = Solution()
print(solution.numDecodings("06"))