from typing import List, Dict, Set, Tuple, Any, Optional
from collections import defaultdict, deque
import copy

class DependencyEngine:
    """
    Deterministic Graph Engine for Onboarding Task Dependencies.
    Handles DAG construction, cycle detection, upstream blocker tracing,
    downstream blast radius calculation, topological sorting, and React Flow formatting.
    """

    @staticmethod
    def detect_cycles(tasks: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Detects if there are any cycles in the dependency graph using DFS.
        Returns (has_cycle, cycle_path).
        """
        adj = defaultdict(list)
        for dep in dependencies:
            adj[dep["depends_on_task_id"]].append(dep["task_id"])

        visited = {} # False = visiting, True = visited
        cycle = []

        def dfs(node, path):
            visited[node] = False
            for neighbor in adj.get(node, []):
                if neighbor in visited and not visited[neighbor]:
                    cycle.extend(path + [neighbor])
                    return True
                if neighbor not in visited:
                    if dfs(neighbor, path + [neighbor]):
                        return True
            visited[node] = True
            return False

        task_ids = [t["id"] for t in tasks]
        for tid in task_ids:
            if tid not in visited:
                if dfs(tid, [tid]):
                    return True, cycle

        return False, []

    @staticmethod
    def get_upstream_blockers(task_id: str, tasks_dict: Dict[str, Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Traces all direct and indirect upstream prerequisite tasks that are NOT completed.
        """
        reverse_adj = defaultdict(list) # task_id -> list of depends_on_task_ids
        for dep in dependencies:
            reverse_adj[dep["task_id"]].append(dep["depends_on_task_id"])

        blockers = []
        visited = set()
        queue = deque(reverse_adj.get(task_id, []))

        while queue:
            upstream_id = queue.popleft()
            if upstream_id in visited:
                continue
            visited.add(upstream_id)

            upstream_task = tasks_dict.get(upstream_id)
            if upstream_task:
                if upstream_task.get("status") != "Completed":
                    blockers.append(upstream_task)
                for next_upstream in reverse_adj.get(upstream_id, []):
                    if next_upstream not in visited:
                        queue.append(next_upstream)

        return blockers

    @staticmethod
    def get_downstream_blast_radius(task_id: str, tasks_dict: Dict[str, Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Finds all downstream tasks that depend directly or transitively on the given task.
        """
        adj = defaultdict(list) # depends_on_task_id -> list of task_ids
        for dep in dependencies:
            adj[dep["depends_on_task_id"]].append(dep["task_id"])

        affected = []
        visited = set()
        queue = deque(adj.get(task_id, []))

        while queue:
            downstream_id = queue.popleft()
            if downstream_id in visited:
                continue
            visited.add(downstream_id)

            downstream_task = tasks_dict.get(downstream_id)
            if downstream_task:
                affected.append(downstream_task)
                for next_downstream in adj.get(downstream_id, []):
                    if next_downstream not in visited:
                        queue.append(next_downstream)

        return affected

    @staticmethod
    def recalculate_task_statuses(tasks: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recalculates status for tasks based on upstream dependencies.
        If any upstream dependency is not 'Completed', the downstream task is set to 'Blocked'
        unless it is already 'Completed'.
        """
        tasks_copy = [dict(t) for t in tasks]
        tasks_dict = {t["id"]: t for t in tasks_copy}

        reverse_adj = defaultdict(list)
        for dep in dependencies:
            reverse_adj[dep["task_id"]].append(dep["depends_on_task_id"])

        for t in tasks_copy:
            if t["status"] == "Completed":
                continue # Completed tasks stay completed

            upstream_ids = reverse_adj.get(t["id"], [])
            has_uncompleted_upstream = False
            upstream_blocker_names = []

            for uid in upstream_ids:
                upstream_t = tasks_dict.get(uid)
                if upstream_t and upstream_t.get("status") != "Completed":
                    has_uncompleted_upstream = True
                    upstream_blocker_names.append(upstream_t.get("name", upstream_t.get("task_id", uid)))

            if has_uncompleted_upstream:
                t["status"] = "Blocked"
                t["delay_reason"] = f"Blocked by uncompleted upstream tasks: {', '.join(upstream_blocker_names)}"
            elif t["status"] == "Blocked":
                # Upstream dependencies resolved, unblock to Pending or In Progress
                t["status"] = "Pending"
                t["delay_reason"] = None

        return tasks_copy

    @staticmethod
    def compute_critical_path(tasks: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[str]:
        """
        Computes the critical path (longest duration path from root to leaf).
        Returns list of task IDs on the critical path.
        """
        if not tasks:
            return []

        adj = defaultdict(list)
        in_degree = defaultdict(int)
        for t in tasks:
            in_degree[t["id"]] = 0

        for dep in dependencies:
            adj[dep["depends_on_task_id"]].append(dep["task_id"])
            in_degree[dep["task_id"]] += 1

        tasks_dict = {t["id"]: t for t in tasks}

        # Topological sort
        zero_in = deque([tid for tid, deg in in_degree.items() if deg == 0])
        dist = {t["id"]: t.get("estimated_duration_days", 1.0) for t in tasks}
        prev = {t["id"]: None for t in tasks}

        while zero_in:
            u = zero_in.popleft()
            for v in adj.get(u, []):
                v_duration = tasks_dict.get(v, {}).get("estimated_duration_days", 1.0)
                if dist[u] + v_duration > dist[v]:
                    dist[v] = dist[u] + v_duration
                    prev[v] = u
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    zero_in.append(v)

        # Node with max distance
        if not dist:
            return []
        max_node = max(dist, key=dist.get)

        path = []
        curr = max_node
        while curr:
            path.append(curr)
            curr = prev[curr]

        path.reverse()
        return path

    @staticmethod
    def build_react_flow_elements(
        employee_id: str,
        tasks: List[Dict[str, Any]],
        dependencies: List[Dict[str, Any]],
        blocked_task_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Converts tasks and dependencies into React Flow nodes and edges with hierarchical layout.
        """
        if blocked_task_ids is None:
            blocked_task_ids = [t["id"] for t in tasks if t.get("status") in ("Blocked", "Delayed")]

        # Compute topological rank/layer for X-positioning
        reverse_adj = defaultdict(list)
        for dep in dependencies:
            reverse_adj[dep["task_id"]].append(dep["depends_on_task_id"])

        rank = {}
        def get_rank(node_id, visited):
            if node_id in rank:
                return rank[node_id]
            if node_id in visited:
                return 0
            visited.add(node_id)
            upstreams = reverse_adj.get(node_id, [])
            if not upstreams:
                r = 0
            else:
                r = 1 + max([get_rank(uid, visited) for uid in upstreams])
            rank[node_id] = r
            return r

        for t in tasks:
            get_rank(t["id"], set())

        # Group by rank to assign Y positions
        rank_groups = defaultdict(list)
        for t in tasks:
            r = rank.get(t["id"], 0)
            rank_groups[r].append(t)

        nodes = []
        for r, group in rank_groups.items():
            for idx, t in enumerate(group):
                x_pos = 100 + r * 300
                y_pos = 80 + idx * 160

                nodes.append({
                    "id": t["id"],
                    "type": "customTaskNode",
                    "position": {"x": float(x_pos), "y": float(y_pos)},
                    "data": {
                        "id": t["id"],
                        "task_id": t.get("task_id", t["id"]),
                        "name": t.get("name", ""),
                        "description": t.get("description", ""),
                        "department": t.get("department", "HR"),
                        "status": t.get("status", "Pending"),
                        "priority": t.get("priority", "Medium"),
                        "assigned_person": t.get("assigned_person", ""),
                        "due_date": t.get("due_date", ""),
                        "is_critical": t.get("is_critical", False),
                        "delay_reason": t.get("delay_reason", ""),
                        "is_blocked": t["id"] in blocked_task_ids,
                    }
                })

        edges = []
        for dep in dependencies:
            src = dep["depends_on_task_id"]
            tgt = dep["task_id"]
            is_blocked_edge = tgt in blocked_task_ids

            edge_data = {
                "id": f"e-{src}-{tgt}",
                "source": src,
                "target": tgt,
                "animated": is_blocked_edge,
                "style": {
                    "stroke": "#ef4444" if is_blocked_edge else "#94a3b8",
                    "strokeWidth": 2.5 if is_blocked_edge else 1.5,
                },
                "markerEnd": {
                    "type": "arrowclosed",
                    "color": "#ef4444" if is_blocked_edge else "#94a3b8"
                }
            }
            edges.append(edge_data)

        return {
            "employee_id": employee_id,
            "nodes": nodes,
            "edges": edges,
            "blocked_task_ids": blocked_task_ids,
            "critical_path_task_ids": DependencyEngine.compute_critical_path(tasks, dependencies),
            "has_cycles": False,
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t.get("status") == "Completed"]),
        }
