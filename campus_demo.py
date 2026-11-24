"""Campus relay delivery. Run: python campus_demo.py"""
from heapq import heappop, heappush

START, GOAL, GATE = (0, 2), (4, 2), (1, 2)
WALLS = {(2, 1), (3, 3)}


def astar(risk):
    """Minimize movement cost plus expected delay at the gate."""
    def distance(cell):
        return abs(cell[0] - GOAL[0]) + abs(cell[1] - GOAL[1])

    queue = [(distance(START), 0, START)]
    cost = {START: 0}
    parent = {}
    while queue:
        _, g, cell = heappop(queue)
        if g != cost[cell]:
            continue
        if cell == GOAL:
            path = [cell]
            while cell in parent:
                cell = parent[cell]
                path.append(cell)
            return path[::-1], g
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            x, y = cell[0] + dx, cell[1] + dy
            nxt = (x, y)
            if not (0 <= x < 5 and 0 <= y < 5) or nxt in WALLS:
                continue
            new_cost = g + 1 + (4 * risk if nxt == GATE else 0)
            if new_cost < cost.get(nxt, float("inf")):
                parent[nxt], cost[nxt] = cell, new_cost
                heappush(queue, (new_cost + distance(nxt), new_cost, nxt))
    return [], float("inf")


def posterior(alert):
    hit, false_alarm = (0.8, 0.2) if alert else (0.2, 0.8)
    evidence = 0.3 * hit + 0.7 * false_alarm
    return 0.3 * hit / evidence


def decision(risk, crosses_gate):
    # One-step model. Move earns +3 if clear and -5 if blocked.
    # Wait costs one turn. Future rewards have zero weight.
    next_risk = risk if crosses_gate else 0
    move, wait = 3 - 8 * next_risk, -1
    return move, wait, "MOVE" if move >= wait else "WAIT"


if __name__ == "__main__":
    for alert in (False, True):
        risk = posterior(alert)
        route, cost = astar(risk)
        direct = decision(risk, True)
        planned = decision(risk, route[1] == GATE)
        print("ALERT" if alert else "CLEAR", f"posterior={risk:.4f}",
              f"cost={cost:.2f}", f"moves={len(route)-1}", route)
        print("Direct corridor:", direct, "Planned first step:", planned)
        assert abs(risk - (24/38 if alert else 6/62)) < 1e-9
        assert len(route)-1 == (6 if alert else 4)
        assert direct[2] == ("WAIT" if alert else "MOVE")
        assert planned[2] == "MOVE"

