import javafx.util.Pair;

import java.util.*;

public class dijkstra {
    public static List<Integer> dijkstra(int src, int dst, Map<Integer, Map<Integer, Double>> matrix) {

        Map<Integer, Double> cost = new HashMap<>(); // the weight map that from src node to every node
        Set<Integer> visited = new HashSet<>(); // the set of nodes visited
        Map<Integer, Integer> preNodeMap = new HashMap<>();  //key:node, val:the preNodeMap of the key;
        // 小根堆
        PriorityQueue<Pair<Integer, Double>> q=new PriorityQueue<>(new Comparator<Pair<Integer, Double>>() {
            @Override
            public int compare(Pair<Integer, Double> o1, Pair<Integer, Double> o2) {
                double x = o1.getValue() - o2.getValue();
                if(x == 0) return 0;
                else if(x > 0) return 1;
                else return -1;
            }
        });
        q.add(makePair(src, 0));
        while (!q.isEmpty()) {
            if (visited.contains(q.peek().getKey())) { // if the node is in visited set, pop it.
                q.poll();
                continue;
            }
            Pair<Integer, Double> pair = q.poll();
//            System.out.println("curr: " + pair.toString());
            int key = pair.getKey();
            double val = pair.getValue();

            visited.add(key);  // put the node in visited set.
            cost.put(key, val);  // update the weight from src to key.
            if (key == dst) break; // find the dst node, return.
            Map<Integer, Double> adjMap = matrix.get(key);
            if (adjMap.isEmpty()) break;
            for (Integer k : adjMap.keySet()) {
                double v = adjMap.get(k);
                if (cost.containsKey(k)) {
                    if (cost.get(k) > v + cost.get(key)) {
                        cost.put(k, v + cost.get(key));
                        preNodeMap.put(k, key);
                    }
                } else {
                    cost.put(k, v + cost.get(key));
                    preNodeMap.put(k, key);
                }
                q.add(makePair(k, cost.get(k)));
            }
        }
        System.out.println("cost: " + cost.toString());
        System.out.println("preNodeMap: " + preNodeMap.toString());
        return findPath(src, dst, preNodeMap);
    }

    // 根据前驱节点逆向打印路径
    public static List<Integer> findPath(int src, int dst, Map<Integer, Integer> map) {
        List<Integer> path = new LinkedList<>();
        int node = dst;
        while (node != src) {
            path.add(0, map.get(node));
            node = map.get(node);

        }
        path.add(dst);
        return path;
    }

    public static Pair<Integer, Double> makePair(int key, double val) {
        return new Pair<>(key, val);
    }

    public static Map<Integer, Map<Integer, Double>> makeMap() {
        Map<Integer, Map<Integer, Double>> map = new HashMap<>();
        Scanner sc = new Scanner(System.in);
        System.out.println("make map: \nn:");
        int n = sc.nextInt();
        System.out.println("u, v, w:");
        for (int i = 0; i < n; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            double w = sc.nextDouble();
            System.out.println();
            Map<Integer, Double> tmp;
            if (map.containsKey(u)) {
                tmp = map.get(u);
                tmp.put(v, w);
                map.put(u, tmp);
            } else {
                tmp = new HashMap<>();
                tmp.put(v, w);
                map.put(u, tmp);
            }

        }
        System.out.println(map.toString());
        return map;
    }
    public static Map<Integer, Map<Integer, Double>> array2Map(int[][] arr) {
        Map<Integer, Map<Integer, Double>> map = new HashMap<>();
        for (int i = 0; i < arr.length; i++) {
            if (map.containsKey(arr[i][0])) {
                Map<Integer, Double> m = map.get(arr[i][0]);
                m.put(arr[i][1], (double)arr[i][2]);
                map.put(arr[i][0], m);
            } else {
                Map<Integer, Double> m = new HashMap<>();
                m.put(arr[i][1], (double)arr[i][2]);
                map.put(arr[i][0], m);
            }
        }
        return map;
    }
    public static void main(String[] args) {
        int[][] arr = {{1,2,12},{1,6,16},{1,7,14},{2,3,10},{2,6,7},{3,4,3},{3,5,5},{3,6,6},
                {4,3,3},{5,3,5},{5,4,4},{6,3,6},{6,5,2},{7,6,9},{7,5,8}};
        Map<Integer, Map<Integer, Double>> map = array2Map(arr); // = makeMap();

//        Scanner sc = new Scanner(System.in);
//        System.out.println("src:");
//        int src = sc.nextInt();
//        System.out.println("dst:");
//        int dst = sc.nextInt();
        System.out.println(dijkstra(1, 4, map));
    }
}
