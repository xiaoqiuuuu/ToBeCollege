"""
    这是一个 16 * 10 的 matrix 类，主要用于处理修改和区间查询操作
    支持修改和重新构建和前缀和优化
"""


class Matrix:
    # 仅支持160长度列表的构建
    def __init__(self, digits):
        self.n = 16
        self.m = 10
        self.matrix = [[0 for _ in range(self.m + 1)] for _ in range(self.n + 1)]
        self.prefix_sum = [[0 for _ in range(self.m + 1)] for _ in range(self.n + 1)]

        for i, digit in enumerate(digits):
            self.matrix[(i // self.m) + 1][i % self.m + 1] = int(digit)
        self.build()

    def query(self, position: tuple):
        x1, y1, x2, y2 = position
        return sum(self.matrix[i][j] for i in range(x1, x2 + 1) for j in range(y1, y2 + 1))

    def modify(self, position: tuple):
        x1, y1, x2, y2 = position
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.matrix[i][j] = 0

    def quick_query(self, position: tuple):
        x1, y1, x2, y2 = position

        return self.prefix_sum[x2][y2] - self.prefix_sum[x1 - 1][y2] - self.prefix_sum[x2][y1 - 1] + \
            self.prefix_sum[x1 - 1][y1 - 1]

    def build(self):
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                self.prefix_sum[i][j] = self.prefix_sum[i - 1][j] + self.prefix_sum[i][j - 1] - self.prefix_sum[i - 1][
                    j - 1] + self.matrix[i][j]

    def show(self):
        for row in self.matrix[1:]:
            print(row[1:])
        print("\n\n\n")
