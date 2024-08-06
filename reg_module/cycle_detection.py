from svgpathtools import svg2paths, Path, Line, CubicBezier, QuadraticBezier, Arc
import numpy as np
import csv
from collections import defaultdict
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

class CycleDetector:
    def __init__(self, updated_curves: dict[int, List[Tuple[float, float]]]):
        self.adj_list, self.segments = self.construct_adj_list(updated_curves)

    def construct_adj_list(self, updated_curves):
        adj_list = defaultdict(list)
        segments = []
        for polyline in updated_curves.values():
            for i in range(len(polyline) - 1):
                start, end = polyline[i], polyline[i + 1]
                adj_list[start].append(end)
                adj_list[end].append(start)
                segments.append((start, end))
        return adj_list, segments

    def find_cycles(self, graph):
        def dfs(node, start, visited, path):
            visited[node] = True
            path.append(node)

            for neighbor in graph[node]:
                if neighbor == start and len(path) > 2:
                    cycle = path[:] + [start]
                    cycles.append(cycle)
                elif not visited[neighbor]:
                    dfs(neighbor, start, visited, path)

            path.pop()
            visited[node] = False

        cycles = []
        visited = defaultdict(bool)

        for node in graph:
            if not visited[node]:
                dfs(node, node, visited, [])

        unique_cycles = []
        for cycle in cycles:
            cycle_set = set(cycle)
            if all(cycle_set != set(c) for c in unique_cycles):
                unique_cycles.append(cycle)

        return unique_cycles

    def separate_non_cycle_lines(self, segments, cycles):
        cycle_edges = set()
        for cycle in cycles:
            for i in range(len(cycle) - 1):
                edge = tuple(sorted([cycle[i], cycle[i + 1]]))
                cycle_edges.add(edge)

        non_cycle_lines = []
        for start, end in segments:
            edge = tuple(sorted([start, end]))
            if edge not in cycle_edges:
                non_cycle_lines.append((start, end))

        return non_cycle_lines

    def process_cycles(self):
        cycles = self.find_cycles(self.adj_list)
        non_cycle_lines = self.separate_non_cycle_lines(self.segments, cycles)
        return cycles, non_cycle_lines
