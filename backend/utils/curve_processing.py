from svgpathtools import svg2paths, Path, Line, CubicBezier, QuadraticBezier, Arc
import numpy as np
import csv
from collections import defaultdict
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

class CurveProcessor:
    def __init__(self, curves: dict[int, List[Tuple[float, float]]], epsilon: float = 5.0, threshold: float = 5.0):
        self.curves = curves
        self.epsilon = epsilon
        self.threshold = threshold
        self.simplified_curves = {}
        self.inverse_dict = {}
        self.segment_points_dict = {}
        self.updated_curves = {}

    def point_line_distance(self, point, start, end):
        point = np.array(point)
        start = np.array(start)
        end = np.array(end)
        
        if np.array_equal(start, end):
            return np.linalg.norm(point - start)
        else:
            n = abs((end[1] - start[1]) * point[0] - (end[0] - start[0]) * point[1] + end[0] * start[1] - end[1] * start[0])
            d = np.linalg.norm(end - start)
            return n / d

    def ramer_douglas_peucker(self, points, epsilon):
        dmax = 0.0
        index = 0
        end = len(points)
        for i in range(1, end - 1):
            # print(points)
            d = self.point_line_distance(points[i], points[0], points[-1])
            if d > dmax:
                index = i
                dmax = d

        if dmax > epsilon:
            rec_results1, idx1 = self.ramer_douglas_peucker(points[:index+1], epsilon)
            rec_results2, idx2 = self.ramer_douglas_peucker(points[index:], epsilon)
            result = rec_results1[:-1] + rec_results2
            result_indices = idx1[:-1] + [i + index for i in idx2]
        else:
            result = [points[0], points[-1]]
            result_indices = [0, len(points) - 1]

        return result, result_indices

    def simplify_curves(self):
        simplified_curves = {}
        inverse_dict = {}
        segment_points_dict = {}
        segment_id = 0

        for index, points in self.curves.items():
            simplified_points, indices = self.ramer_douglas_peucker(points, self.epsilon)

            for i in range(len(simplified_points) - 1):
                start_point = tuple(simplified_points[i])
                end_point = tuple(simplified_points[i + 1])
                line_key = (start_point, end_point)

                segment_indices = indices[i:i+2]
                segment_start_idx = segment_indices[0]
                segment_end_idx = segment_indices[1]

                simplified_curves[segment_id] = [start_point, end_point]
                inverse_dict[line_key] = segment_id
                segment_points_dict[segment_id] = points[segment_start_idx:segment_end_idx+1]

                segment_id += 1

        self.simplified_curves = simplified_curves
        self.inverse_dict = inverse_dict
        self.segment_points_dict = segment_points_dict

    def distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))

    def midpoint(self, point1, point2):
        return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    def round_point(self, point):
        return (round(point[0], 1), round(point[1], 1))

    def update_endpoints_with_midpoints(self):
        endpoints = {}
        updated_curves = {k: v[:] for k, v in self.simplified_curves.items()}
        inverse_dict = {}

        for key, points in self.simplified_curves.items():
            endpoints[key] = (points[0], points[-1])

        for key, (start, end) in endpoints.items():
            if self.distance(start, end) < self.threshold:
                mid = self.midpoint(start, end)
                updated_curves[key][0] = mid
                updated_curves[key][-1] = mid

        for key1, (start1, end1) in endpoints.items():
            for key2, (start2, end2) in endpoints.items():
                if key1 < key2:
                    if self.distance(start1, start2) < self.threshold:
                        mid = self.midpoint(start1, start2)
                        updated_curves[key1][0] = mid
                        updated_curves[key2][0] = mid
                    if self.distance(start1, end2) < self.threshold:
                        mid = self.midpoint(start1, end2)
                        updated_curves[key1][0] = mid
                        updated_curves[key2][-1] = mid
                    if self.distance(end1, start2) < self.threshold:
                        mid = self.midpoint(end1, start2)
                        updated_curves[key1][-1] = mid
                        updated_curves[key2][0] = mid
                    if self.distance(end1, end2) < self.threshold:
                        mid = self.midpoint(end1, end2)
                        updated_curves[key1][-1] = mid
                        updated_curves[key2][-1] = mid

        for key, points in updated_curves.items():
            updated_curves[key] = [self.round_point(point) for point in points]

        for index, points in updated_curves.items():
            for i in range(len(points) - 1):
                start_point = tuple(points[i])
                end_point = tuple(points[i + 1])
                line_key = (start_point, end_point)
                inverse_dict[line_key] = index

        self.updated_curves = updated_curves
        self.inverse_dict = inverse_dict

    def plot_segments(self, curves, inverse_dict, title):
        plt.figure(figsize=(10, 6))
        for (start, end), segment_id in inverse_dict.items():
            x = [start[0], end[0]]
            y = [start[1], end[1]]
            plt.plot(x, y, marker='o', label=f'Segment {segment_id}')
        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_points(self, curves, title):
        plt.figure(figsize=(10, 6))
        for points in curves.values():
            x, y = zip(*points)
            plt.plot(x, y, marker='o', linestyle='None')
        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()

    def process(self):
        self.simplify_curves()
        self.update_endpoints_with_midpoints()
        # self.plot_segments(self.simplified_curves, self.inverse_dict, "Original Simplified Curves")
        # self.plot_segments(self.updated_curves, self.inverse_dict, "Updated Curves")
        # self.plot_points(self.updated_curves, "Points in Updated Curves")
