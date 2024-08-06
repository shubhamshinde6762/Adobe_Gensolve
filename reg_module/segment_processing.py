import matplotlib.pyplot as plt
import numpy as np

def are_approximately_equal(p1, p2, tol=5):
    return np.linalg.norm(np.array(p1) - np.array(p2)) < tol

def compute_slope(p1, p2):
    if p2[0] == p1[0]:
        return np.inf
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

class SegmentProcessor:
    def __init__(self, segments, tol=1):
        self.segments = segments
        self.tol = tol
        self.merged_segments = []
        self.map = {}
        self.common_vertex_segments = []
        self.filtered_merged_segments = []

    def merge_collinear_segments(self):
        merged_segments = []
        used = set()
        segment_map = {}
        
        while len(used) < len(self.segments):
            for i, (start1, end1) in enumerate(self.segments):
                if i not in used:
                    break

            collinear_group = [(start1, end1)]
            used.add(i)

            while True:
                merged = False
                for j, (start2, end2) in enumerate(self.segments):
                    if j in used:
                        continue
                    
                    if (np.abs(compute_slope(start1, end1) - compute_slope(start2, end2)) < self.tol):
                        if any(are_approximately_equal(start, start2) or 
                               are_approximately_equal(start, end2) or
                               are_approximately_equal(end, start2) or 
                               are_approximately_equal(end, end2) for start, end in collinear_group):
                            collinear_group.append((start2, end2))
                            used.add(j)
                            merged = True

                if not merged:
                    break

            all_points = np.array([point for segment in collinear_group for point in segment])
            min_idx = np.argmin(all_points[:, 0])
            max_idx = np.argmax(all_points[:, 0])
            min_y_idx = np.argmin(all_points[:, 1])
            max_y_idx = np.argmax(all_points[:, 1])

            if np.abs(compute_slope(start1, end1)) < self.tol:
                merged_segments.append((tuple(all_points[min_idx]), tuple(all_points[max_idx])))
                segment_map[(tuple(all_points[min_idx]), tuple(all_points[max_idx]))] = collinear_group
            else:
                segment_map[(tuple(all_points[min_y_idx]), tuple(all_points[max_y_idx]))] = collinear_group
                merged_segments.append((tuple(all_points[min_y_idx]), tuple(all_points[max_y_idx])))

        self.merged_segments = merged_segments
        self.map = segment_map

    def find_segments_with_common_vertices(self):
        common_vertex_segments = []
        for i, (start1, end1) in enumerate(self.merged_segments):
            for j, (start2, end2) in enumerate(self.merged_segments):
                if i != j:
                    if are_approximately_equal(start1, start2, self.tol) or are_approximately_equal(start1, end2, self.tol) or \
                       are_approximately_equal(end1, start2, self.tol) or are_approximately_equal(end1, end2, self.tol):
                        common_vertex_segments.append((start1, end1))
                        break
        self.common_vertex_segments = common_vertex_segments

    def revert_to_original_segments(self):
        reverted_segments = []
        for segment in self.common_vertex_segments:
            reverted_segments += self.map[segment]
        return reverted_segments

    def filter_merged_segments(self):
        self.filtered_merged_segments = [seg for seg in self.merged_segments if seg not in self.common_vertex_segments]

    def plot_segments(self, segments, title, highlight_segments=None):
        plt.figure(figsize=(10, 8))
        for (start, end) in segments:
            plt.plot([start[0], end[0]], [start[1], end[1]], marker='o', color='blue')
        if highlight_segments:
            for (start, end) in highlight_segments:
                plt.plot([start[0], end[0]], [start[1], end[1]], marker='o', color='red')
        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()


