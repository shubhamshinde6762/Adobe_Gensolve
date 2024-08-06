from svgpathtools import svg2paths, Path, Line, CubicBezier, QuadraticBezier, Arc
import numpy as np
import csv
from collections import defaultdict
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import heapq


class CircleDetector:
    def __init__(self, unique_cycles):
        self.unique_cycles = unique_cycles
        self.remaining_sides = set()
        self.marked_sides = set()

    def point_to_segment_dist(self, p, v, w):
        l2 = np.sum((v - w) ** 2)
        if l2 == 0:
            return np.sum((p - v) ** 2)
        t = max(0, min(1, np.dot(p - v, w - v) / l2))
        projection = v + t * (w - v)
        return np.sum((p - projection) ** 2)

    def mean_square_circle_error(self, polygon, center, radius, num_points=100):
        total_error = 0
        total_samples = 0

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            segment_points = np.linspace(p1, p2, num_points)

            for point in segment_points:
                closest_point = self.closest_point_on_circle(point, center, radius)
                dist = np.linalg.norm(point - closest_point)
                error = dist ** 2
                total_error += error

            total_samples += len(segment_points)

        mse = total_error / total_samples
        return mse

    def closest_point_on_circle(self, point, center, radius):
        direction = point - center
        direction /= np.linalg.norm(direction)
        return center + direction * radius

    def best_fit_circle(self, polygon):
        polygon = np.array(polygon)

        best_mse = float('inf')
        best_center = None
        best_radius = None

        for _ in range(100):  # Number of iterations
            sample_indices = np.random.choice(len(polygon), 3, replace=False)
            sample_points = polygon[sample_indices]

            A = sample_points[0]
            B = sample_points[1]
            C = sample_points[2]

            D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))
            if D == 0:
                continue

            Ux = ((A[0]**2 + A[1]**2) * (B[1] - C[1]) + (B[0]**2 + B[1]**2) * (C[1] - A[1]) + (C[0]**2 + C[1]**2) * (A[1] - B[1])) / D
            Uy = ((A[0]**2 + A[1]**2) * (C[0] - B[0]) + (B[0]**2 + B[1]**2) * (A[0] - C[0]) + (C[0]**2 + C[1]**2) * (B[0] - A[0])) / D
            center = np.array([Ux, Uy])
            radius = np.linalg.norm(center - A)

            mse = self.mean_square_circle_error(polygon, center, radius)
            if mse < best_mse:
                best_mse = mse
                best_center = center
                best_radius = radius

        return best_center, best_radius, best_mse

    def plot_polygon_and_circle(self, polygon, center, radius, label):
        polygon = np.array(polygon)  # Ensure polygon is a numpy array
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = center[0] + radius * np.cos(theta)
        circle_y = center[1] + radius * np.sin(theta)

        plt.plot(circle_x, circle_y, 'r--', label=label)
        plt.scatter(*center, color='green', zorder=5, label='Center')

    def plot_remaining_sides(self, unique_cycles, marked_sides):
        for polygon in unique_cycles:
            polygon = np.array(polygon)
            for i in range(len(polygon)):
                side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
                if side not in marked_sides:
                    plt.plot(*np.array([polygon[i], polygon[(i + 1) % len(polygon)]]).T, 'k-', label='Remaining Side' if i == 0 else "")

    def detect_circles(self):
        min_heap = []
        possible_circles = []
        unused_loops = []

        for polygon in self.unique_cycles:
            center, radius, mse = self.best_fit_circle(polygon)
            heapq.heappush(min_heap, (mse, center, radius, polygon))

        while min_heap:
            mse, center, radius, polygon = heapq.heappop(min_heap)

            contains_marked_side = False
            for i in range(len(polygon)):
                side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
                if side in self.marked_sides:
                    contains_marked_side = True
                    break

            if contains_marked_side:
                unused_loops.append(polygon)
                continue

            # self.plot_polygon_and_circle(polygon, center, radius, label='Best Fit Circle')
            # self.plot_remaining_sides(self.unique_cycles, self.marked_sides)
            # plt.legend()
            # plt.axis('equal')
            # plt.show()
            # print(mse)
            if mse < 75:
                # print(f'Mean Square Fitting Error: {mse:.4f}')
                possible_circles.append((center, radius, polygon))

                for i in range(len(polygon)):
                    side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
                    self.marked_sides.add(side)
            else:
                unused_loops.append(polygon)

        filtered_unused_loops = []
        for loop in unused_loops:
            all_sides_unused = True
            for i in range(len(loop)):
                side = tuple(sorted([tuple(loop[i]), tuple(loop[(i + 1) % len(loop)])]))
                if side in self.marked_sides:
                    all_sides_unused = False
                    break
            if all_sides_unused:
                filtered_unused_loops.append(loop)

        # plt.figure()

        # self.plot_remaining_sides(self.unique_cycles, self.marked_sides)
        for polygon in self.unique_cycles:
            polygon = np.array(polygon)
            for i in range(len(polygon)):
                side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
                if side not in self.marked_sides:
                    self.remaining_sides.add(side)

        self.remaining_sides = set([
            ((float(x1), float(y1)), (float(x2), float(y2)))
            for ((x1, y1), (x2, y2)) in self.remaining_sides
        ])

        # for center, radius, polygon in possible_circles:
        #     self.plot_polygon_and_circle(polygon, center, radius, label='Best Fit Circle')

        # plt.legend()
        # plt.axis('equal')
        # plt.show()

        return filtered_unused_loops, possible_circles
