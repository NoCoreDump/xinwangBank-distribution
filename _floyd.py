inf = 9999

def floyd(matrix):

    if matrix is None:
        return None
    crosses_num = len(matrix)
    # floyd算法核心代码
    for k in range(crosses_num):
        for i in range(crosses_num):
            for j in range(crosses_num):
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    # mid_vertex[i]={j:k}
    return matrix

# 测试数据
if __name__ == '__main__':
    matrix = [[1, 2, 10],
              [2, 3, 21],
              [3, 2, 2]]
    matrix = floyd(matrix)
    print(matrix)

