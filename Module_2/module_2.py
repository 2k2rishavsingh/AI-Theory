import math
import heapq
import random
import matplotlib.pyplot as plt

# ---------------------------
# 1. Construct ALWAYS-CONNECTED farm graph (KNN)
# ---------------------------

NUM_NODES = 50
K = 5                        # number of nearest neighbors per node
random.seed(42)

# Random positions in 1000m × 1000m field
positions = {
    i: (random.uniform(0, 1000), random.uniform(0, 1000))
    for i in range(NUM_NODES)
}

def euclidean(a, b):
    ax, ay = a
    bx, by = b
    return math.hypot(ax - bx, ay - by)

# Edge cost parameters
alpha = 1.0
beta = 0.5
gamma = 0.3
delta = 0.2
v = 10.0  # speed m/s

graph = {i: [] for i in range(NUM_NODES)}

# Build KNN graph so it is (with high probability) connected
for i in range(NUM_NODES):
    dists = []
    for j in range(NUM_NODES):
        if i != j:
            dists.append((euclidean(positions[i], positions[j]), j))
    dists.sort()

    for k in range(K):
        j = dists[k][1]
        d = dists[k][0]

        battery_factor = random.uniform(1.0, 2.0)
        wind_factor = random.uniform(0.0, 1.0)
        slope_factor = random.uniform(0.0, 1.0)
        time_ij = d / v

        cost_ij = (alpha * time_ij +
                   beta * battery_factor +
                   gamma * wind_factor +
                   delta * slope_factor)

        graph[i].append((j, cost_ij))
        graph[j].append((i, cost_ij))

# ---------------------------
# 2. UCS
# ---------------------------

def uniform_cost_search(graph, start, goal):
    frontier = [(0.0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0.0}
    expanded = 0

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        expanded += 1

        if current == goal:
            break

        for neighbor, edge_cost in graph[current]:
            new_cost = current_cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return None, float('inf'), expanded

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

    return path, cost_so_far[goal], expanded

# ---------------------------
# 3. A* with admissible heuristic
# ---------------------------

v_max = v
battery_min = 1.0
wind_min = 0.0
slope_min = 0.0

c_min = alpha * (1.0 / v_max) + beta * battery_min

def heuristic(node, goal):
    return euclidean(positions[node], positions[goal]) * c_min

def astar_search(graph, start, goal):
    frontier = [(0.0, start)]
    came_from = {start: None}
    g_cost = {start: 0.0}
    expanded = 0

    while frontier:
        f_current, current = heapq.heappop(frontier)
        expanded += 1

        if current == goal:
            break

        for neighbor, edge_cost in graph[current]:
            tentative_g = g_cost[current] + edge_cost
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_neighbor = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_neighbor, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return None, float('inf'), expanded

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

    return path, g_cost[goal], expanded

# ---------------------------
# 4. Run searches
# ---------------------------

start, goal = 0, 49
ucs_path, ucs_cost, ucs_expanded = uniform_cost_search(graph, start, goal)
astar_path, astar_cost, astar_expanded = astar_search(graph, start, goal)

print("UCS path:", ucs_path, "cost:", ucs_cost, "expanded:", ucs_expanded)
print("A*  path:", astar_path, "cost:", astar_cost, "expanded:", astar_expanded)

# ---------------------------
# 5. Visualization
# ---------------------------

fig, ax = plt.subplots()

# Plot all farm plots
xs = [positions[i][0] for i in range(NUM_NODES)]
ys = [positions[i][1] for i in range(NUM_NODES)]
ax.scatter(xs, ys, marker='o')

# Label nodes
for i in range(NUM_NODES):
    ax.text(positions[i][0] + 5, positions[i][1] + 5, str(i), fontsize=8)

# Draw UCS path
if ucs_path is not None:
    ucs_x = [positions[n][0] for n in ucs_path]
    ucs_y = [positions[n][1] for n in ucs_path]
    ax.plot(ucs_x, ucs_y, linestyle='--', label='UCS path')

# Draw A* path
if astar_path is not None:
    astar_x = [positions[n][0] for n in astar_path]
    astar_y = [positions[n][1] for n in astar_path]
    ax.plot(astar_x, astar_y, linestyle='-', label='A* path')

# Highlight start and goal
ax.scatter([positions[start][0]], [positions[start][1]], marker='s', s=80)
ax.scatter([positions[goal][0]], [positions[goal][1]], marker='^', s=80)

ax.set_xlabel('X position (m)')
ax.set_ylabel('Y position (m)')
ax.set_title('Farm Plots with UCS and A* Paths')
ax.legend()
plt.tight_layout()
plt.show()
