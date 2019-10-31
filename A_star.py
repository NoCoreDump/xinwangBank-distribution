# A* 算法

import numpy as np
import copy

inf = 9999

class car_node():
    def __init__(self,l):
        self.car_id = l[0]
        self.car_from = l[1]
        self.car_to = l[2]
        self.speed = l[3]
        self.palntime = l[4]
        self.start_time = self.palntime


def h(i,j,f_weight_matrix):  # f_weight_matrix: Floyd算法求得的权值矩阵
    return f_weight_matrix[i][j] # 返回任意两点最短路径的总权值，作为估值函数


def path_find(src, dest, pre_nodes, path):
    if pre_nodes[dest] == src:
        path.append(dest+1)
        path.append(src+1)
    else:
        path.append(dest+1)
        path_find(src, pre_nodes[dest], pre_nodes, path)
    return path


def A_star(crosses_num, M, car, f_weight_matrix):
    matrix = M.map_table
    index_matrix = M.cross_list
    if matrix is None:
        return None
    map = [[] for i in range(len(matrix))]
    road_weight = car.map_road_weight
    for i in range(len(matrix)):
        map[i].append(matrix[i][0])
        map[i].append(matrix[i][1])
        map[i].append(road_weight[i][1])
    dis = []
    path = []
    src = index_matrix.index(car.car_from)
    dest = index_matrix.index(car.car_to)
    closed = set()  # 表示已经访问过的节点集合
    opened = []  # 表示当前需要遍历的节点及其F值：(i, fi)
    openlist = []  # 表示当前需要遍历的节点集合
    pre_node = {src: []}
    distance = {src: 0}  # 其他点到出发点的距离，会不断更新
    for i in range(crosses_num):
        dis += [[]]
        for j in range(crosses_num):
            if i == j:
                dis[i].append(0)
            else:
                dis[i].append(inf)
    # 初始化矩阵时，为每一个点计算它到目标点的估值，即:dis[i][dest]+H
    # F = G + H = dis + H
    for i in range(len(matrix)):
        x = map[i][0] - 1
        y = map[i][1] - 1
        dis[x][y] = map[i][2]
    nodes = set()
    for i in range(crosses_num): # 获取图中所有节点，表示还未访问的节点集合
        nodes.add(i)
    for i in nodes:
        distance[i] = dis[src][i]
    if src in nodes:
        opened.append((src,h(src,dest,f_weight_matrix)))
        openlist.append(src)
        nodes.remove(src)
    else:
        return None

    while 1:
        next = opened[0]
        v = next[0]
        opened.remove(next)
        openlist.remove(v)
        closed.add(v)
        if v == dest:
            break
        for i in range(crosses_num):  # v 点的邻接点
            if dis[v][i] != 0 and dis[v][i] != inf:
                if i in closed: # 如果在集合closed中，忽略
                    continue
                elif i in openlist:
                    distance[i] = distance[v] + dis[v][i] # 此处有问题，distance未更新
                    fi = distance[i] + h(i, dest, f_weight_matrix)
                    for old_f in opened:
                        if old_f[0] == i and old_f[1] > fi:
                            pre_node[i] = v
                            opened.remove(old_f)
                            opened.append((i, fi))
                            break
                        else:
                            continue
                else:
                    distance[i] = distance[v] + dis[v][i]
                    fi = distance[i] + h(i, dest, f_weight_matrix)
                    pre_node[i] = v
                    opened.append((i,fi))
                    openlist.append(i)
            else:
                continue
        opened = sorted(opened, key=lambda x :x[1], reverse=False)
    path = path_find(src, dest, pre_node, path)
    path = path[::-1]  # 逆序
    path.append(car.car_from)
    path_shortest = []
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        # print('start, end ')
        # print(start, end)
        for j in range(len(matrix)):
            x = matrix[j][0]
            y = matrix[j][1]
            if start == x and end == y:
                # print('x, y; ')
                # print(x, y)
                path_shortest.append(matrix[j][2])
                break
            else:
                continue
    # print()
    # return car_id, distance[dest], path_shortest # car_id, 最短路径权重，最短路径road_id
    l = len(car.trace)
    flag = 0
    for i in range(4):
        if car.incross:
            road = car.incross[0].orient[1][i]
        else:
            road = car.trace[0].endnode.orient[1][i]
        if road:
            if road.road_id == path_shortest[0]:
                if l <= 1:
                    car.trace.append(road)
                else:
                    car.trace[1] = road
                    car.trace[1] = road
                flag = 1
    if not flag:
        print("No such way!")
    return distance[dest],path


#
# if __name__ == '__main__':
#     matrix = [[1, 2, 1001],
#               [2, 3, 2001],
#               [3, 4, 3001],
#               [1, 3, 4001],
#               [2, 4, 5001]]
#     road_weight = [[1001, 2],
#                    [2001, 3],
#                    [3001, 4],
#                    [4001, 8],
#                    [5001, 12]]
#     car = car_node([10001, 1, 4, 5, 1, 1])
#     distance,path = A_star(4,matrix,road_weight,car)
#
#     print(distance,path)
#
