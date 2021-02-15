class Solution:
    def flip_game(self, s):
        return [s[:idx] + '--' + s[idx+2:] for idx in range(len(s) - 1) if s[idx:idx+2] == '++']
