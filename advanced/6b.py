# State space representation based on diagram map (a)
state_space = {
    "Glogow": {"Leszno": 45},
    "Leszno": {"Glogow": 45, "Poznan": 90, "Wroclaw": 100},
    "Poznan": {"Leszno": 90, "Bydgoszcz": 140},
    "Bydgoszcz": {"Poznan": 140, "Wloclawek": 120},
    "Wloclawek": {"Bydgoszcz": 120, "Plock": 55},
    "Plock": {"Wloclawek": 55, "Warsaw": 130},
    "Warsaw": {"Plock": 130, "Radom": 105},
    "Radom": {"Warsaw": 105, "Kielce": 82},
    "Kielce": {"Radom": 82, "Krakow": 120},
    "Krakow": {"Kielce": 120, "Katowice": 85},
    "Katowice": {"Krakow": 85, "Czestochowa": 80},
    "Czestochowa": {"Katowice": 80, "Kalisz": 118},
    "Kalisz": {"Czestochowa": 118, "Konin": 120},
    "Konin": {"Kalisz": 120, "Lodz": 165},
    "Lodz": {"Konin": 165, "Warsaw": 150}
}

# Breadth-First Search (BFS) implementation

def bfs(state_space, start, goal):
    open_list = [start]  # Queue for BFS
    closed_list = []  # Visited nodes

    while open_list:
        current = open_list.pop(0)  # Get the first element from the queue
        closed_list.append(current)  # Mark as visited

        print(f"Visiting: {current}")

        if current == goal:
            print("Goal reached!")
            return closed_list

        # Add neighbors to the queue
        for neighbor in state_space[current]:
            if neighbor not in closed_list and neighbor not in open_list:
                open_list.append(neighbor)

    print("Goal not reachable.")
    return closed_list

# Example usage
start_city = "Glogow"
goal_city = "Plock"
path = bfs(state_space, start_city, goal_city)
print(f"Path from {start_city} to {goal_city}: {path}")