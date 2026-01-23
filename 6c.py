# State space representation based on diagram map (b)
state_space = {
    "Glogow": {"Leszno": 40},
    "Leszno": {"Glogow": 40, "Poznan": 67, "Wroclaw": 87},
    "Poznan": {"Leszno": 67, "Bydgoszcz": 108},
    "Bydgoszcz": {"Poznan": 108, "Wloclawek": 102},
    "Wloclawek": {"Bydgoszcz": 102, "Plock": 44},
    "Plock": {"Wloclawek": 44, "Warsaw": 95},
    "Warsaw": {"Plock": 95, "Radom": 91},
    "Radom": {"Warsaw": 91, "Kielce": 70},
    "Kielce": {"Radom": 70, "Krakow": 102},
    "Krakow": {"Kielce": 102, "Katowice": 68},
    "Katowice": {"Krakow": 68, "Czestochowa": 61},
    "Czestochowa": {"Katowice": 61, "Kalisz": 90},
    "Kalisz": {"Czestochowa": 90, "Konin": 95},
    "Konin": {"Kalisz": 95, "Lodz": 118},
    "Lodz": {"Konin": 118, "Warsaw": 124}
}

# Heuristic function based on straight-line distances
heuristic = {
    "Glogow": 40,
    "Leszno": 67,
    "Poznan": 108,
    "Bydgoszcz": 90,
    "Wloclawek": 44,
    "Plock": 0,  # Goal node
    "Warsaw": 95,
    "Radom": 91,
    "Kielce": 70,
    "Krakow": 102,
    "Katowice": 68,
    "Czestochowa": 61,
    "Kalisz": 90,
    "Konin": 95,
    "Lodz": 118
}

# A* Search implementation

def a_star(state_space, heuristic, start, goal):
    open_list = [(start, 0)]  # Priority queue with (node, cost)
    closed_list = []  # Visited nodes
    g_costs = {start: 0}  # Cost from start to current node

    while open_list:
        # Sort by total estimated cost (g + h)
        open_list.sort(key=lambda x: g_costs[x[0]] + heuristic[x[0]])
        current, _ = open_list.pop(0)  # Get the node with the lowest cost
        closed_list.append(current)

        print(f"Visiting: {current}")

        if current == goal:
            print("Goal reached!")
            return closed_list

        # Add neighbors to the priority queue
        for neighbor, cost in state_space[current].items():
            if neighbor not in closed_list:
                tentative_g_cost = g_costs[current] + cost
                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    open_list.append((neighbor, tentative_g_cost))

    print("Goal not reachable.")
    return closed_list

# Example usage
start_city = "Glogow"
goal_city = "Plock"
path = a_star(state_space, heuristic, start_city, goal_city)
print(f"Path from {start_city} to {goal_city}: {path}")