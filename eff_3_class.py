import sys
import time
import psutil

class SequenceAlignment:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.delta = 30
        self.alpha = {
            ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
            ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
            ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
            ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
        }

    def read_sequences(self):
        with open(self.input_file_path, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip()
            for i in range(len(lines)):
                if lines[i].isdigit():
                    lines[i] = int(lines[i])

            base_string_indices = []
            for i, element in enumerate(lines):
                if isinstance(element, str):
                    base_string_indices.append(i)
            base_string1 = lines[base_string_indices[0]]
            base_string2 = lines[base_string_indices[1]]
            nums1 = lines[base_string_indices[0] + 1:base_string_indices[1]]
            nums2 = lines[base_string_indices[1] + 1:]

            for i in nums1:
                base_string1 = base_string1[:i + 1] + base_string1 + base_string1[i + 1:]
            for i in nums2:
                base_string2 = base_string2[:i + 1] + base_string2 + base_string2[i + 1:]

            return base_string1, base_string2

    def calculate_cost(self, s1_sol, s2_sol):
        cost = 0
        for i, j in zip(s1_sol, s2_sol):
            if i == '_':
                cost += self.delta
            elif j == '_':
                cost += self.delta
            elif i != '_' and j != '_':
                cost += self.alpha[(i, j)]
        return cost

    def process_memory(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_consumed = int(memory_info.rss / 1024)
        return memory_consumed

    def backtrack(self, dp, s1, s2, s1_len, s2_len):
        s1_sol = ''
        s2_sol = ''
        i = s1_len
        j = s2_len

        while i != 0 and j != 0:
            cost = dp[i][j]
            if cost == dp[i - 1][j - 1] + self.alpha[(s1[i - 1], s2[j - 1])]:
                s1_sol = s1_sol + s1[i - 1]
                s2_sol = s2_sol + s2[j - 1]
                i = i - 1
                j = j - 1
            elif cost == dp[i - 1][j] + self.delta:
                s1_sol = s1_sol + s1[i - 1]
                s2_sol = s2_sol + '_'
                i = i - 1
            elif cost == dp[i][j - 1] + self.delta:
                s1_sol = s1_sol + '_'
                s2_sol = s2_sol + s2[j - 1]
                j = j - 1

        if i != 0 and j == 0:
            while i != 0:
                s2_sol = s2_sol + '_'
                s1_sol = s1_sol + s1[i - 1]
                i = i - 1
        if j != 0 and i == 0:
            while j != 0:
                s1_sol = s1_sol + '_'
                s2_sol = s2_sol + s2[j - 1]
                j = j - 1

        return s1_sol[::-1], s2_sol[::-1]

    def basic_dp(self, s1, s2):
        s1_l = len(s1)
        s2_l = len(s2)

        dp = [[0] * (s2_l + 1) for _ in range(s1_l + 1)]

        for i in range(s1_l + 1):
            dp[i][0] = self.delta * i
        for j in range(s2_l + 1):
            dp[0][j] = self.delta * j

        for i in range(1, s1_l + 1):
            for j in range(1, s2_l + 1):
                dp[i][j] = min(dp[i - 1][j - 1] + self.alpha[(s1[i - 1], s2[j - 1])],
                               dp[i - 1][j] + self.delta,
                               dp[i][j - 1] + self.delta)

        s1_sol, s2_sol = self.backtrack(dp, s1, s2, s1_l, s2_l)
        return dp[s1_l][s2_l], s1_sol, s2_sol

    def space_efficient_alignment(self, s1, s2):
        s1_l = len(s1)
        s2_l = len(s2)

        dp = [[0, 0] for _ in range(s1_l + 1)]

        for i in range(s1_l + 1):
            dp[i][0] = self.delta * i

        for j in range(1, s2_l + 1):
            dp[0][1] = self.delta * j
            for i in range(1, s1_l + 1):
                dp[i][1] = min(dp[i - 1][0] + self.alpha[(s1[i - 1], s2[j - 1])],
                               dp[i - 1][1] + self.delta,
                               dp[i][0] + self.delta)
            for row in dp:
                row[0], row[1] = row[1], 0

        row = [row[0] for row in dp]
        return dp[s1_l][0], row

    def divide_conquer(self, s1, s2):
        s1_l = len(s1)
        s2_l = len(s2)

        if s1_l <= 2 or s2_l <= 2:
            cost, s1_sol, s2_sol = self.basic_dp(s1, s2)
            return s1_sol, s2_sol

        split_point = int(s1_l / 2)
        forward_s1 = s1[0:split_point]
        rev_s1 = s1[split_point:]

        cost_forward, column_forward = self.space_efficient_alignment(s2, forward_s1)
        cost_backward, column_backward = self.space_efficient_alignment(s2[::-1], rev_s1[::-1])

        column_backward = column_backward[::-1]
        cost = float('inf')

        for i in range(len(column_forward)):
            if column_backward[i] + column_forward[i] <= cost:
                cost = column_backward[i] + column_forward[i]
                opt_choice = i

        forward_s2 = s2[0:opt_choice]
        rev_s2 = s2[opt_choice:]

        forward_s2_res, forward_s1_res = self.divide_conquer(forward_s1, forward_s2)
        rev_s2_res, rev_s1_res = self.divide_conquer(rev_s1, rev_s2)

        return forward_s2_res + rev_s2_res, forward_s1_res + rev_s1_res

    def align_sequences(self):
        s1, s2 = self.read_sequences()

        start_time = time.time()
        result = self.divide_conquer(s1, s2)
        cost = self.calculate_cost(result[0], result[1])
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # in ms

        memory_consumed = self.process_memory()  # in KB

        with open(self.output_file_path, 'w') as file:
            file.write(str(cost) + '\n')
            file.write(result[0] + '\n')
            file.write(result[1] + '\n')
            file.write(str(total_time) + '\n')
            file.write(str(memory_consumed))

        print(f'm+n = {len(s1) + len(s2)}')
        print(f'cost = {cost}')
        print(f'time = {total_time}')
        print(f'memory = {memory_consumed}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python script.py input_file output_file')
    else:
        alignment = SequenceAlignment(sys.argv[1], sys.argv[2])
        alignment.align_sequences()

