import math
import heapq
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

class PolygonDetection:
    def __init__(self, error_threshold=150):
        self.error_threshold = error_threshold
        
    def sample_points_along_segment(self, p1, p2, num_points=30):
        return np.linspace(p1, p2, num_points)

    def calculate_angle_between_lines(self, line1, line2):
        def vector_from_line(line):
            (x1, y1), (x2, y2) = line
            return (x2 - x1, y2 - y1)

        common_points = set(line1) & set(line2)
        if len(common_points) == 0:
            return None

        vec1 = vector_from_line(line1)
        vec2 = vector_from_line(line2)

        magnitude1 = math.sqrt(vec1[0]**2 + vec1[1]**2)
        magnitude2 = math.sqrt(vec2[0]**2 + vec2[1]**2)

        if magnitude1 == 0 or magnitude2 == 0:
            return None

        dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
        cos_theta = dot_product / (magnitude1 * magnitude2)

        cos_theta = min(1, max(-1, cos_theta))

        angle = math.degrees(math.acos(cos_theta))
        return angle

    def are_points_close(self, p1, p2, tolerance=1):
        return np.linalg.norm(np.array(p1) - np.array(p2)) < tolerance

    def calculate_area_contribution(self, p1, p2, p3):
        """Calculate the signed area of the triangle formed by p1, p2, p3."""
        return 0.5 * abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))

    def calculate_internal_angle(self, p1, p2, p3):
        vec1 = np.array(p2) - np.array(p1)
        vec2 = np.array(p3) - np.array(p2)
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        cos_theta = dot_product / (magnitude1 * magnitude2)
        cos_theta = min(1, max(-1, cos_theta))
        return math.degrees(math.acos(cos_theta))

    def process_polygons(self, polygons):
        vertices_arr = []
        lines_arr = []

        for points in polygons:
            lines = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]

            # Step 1: Remove vertices forming concave angles
            concave_vertices = []
            for i in range(len(points)):
                p_prev = points[i - 1]
                p_curr = points[i]
                p_next = points[(i + 1) % len(points)]
                angle = self.calculate_internal_angle(p_prev, p_curr, p_next)
                if angle > 180:
                    concave_vertices.append(p_curr)

            points = [p for p in points if p not in concave_vertices]

            # Step 2: Filter vertices with distance logic
            points = self.filter_points(np.array(points))

            # Step 3: Area contribution logic
            heap = []
            for i in range(len(points)):
                p_prev = points[i - 1]
                p_curr = points[i]
                p_next = points[(i + 1) % len(points)]
                area_contribution = self.calculate_area_contribution(p_prev, p_curr, p_next)
                heapq.heappush(heap, (-area_contribution, p_curr))

            vertices = set()
            while heap:
                score, vertex = heapq.heappop(heap)
                vertex_tuple = tuple(vertex)  # Convert numpy array to a tuple
                if not any(self.are_points_close(vertex, np.array(v)) for v in vertices):
                    vertices.add(vertex_tuple)

            vertices = np.array([np.array(v) for v in vertices])
            vertices = self.filter_points(vertices)

            # Step 4: Check if remaining vertices have nearly the same angles
            centroid = np.mean(vertices, axis=0)
            angles = [self.calculate_angle(v, centroid) for v in vertices]
            avg_angle = np.mean(angles)
            angle_deviation = np.std(angles)

            # Remove vertices that deviate significantly from the average angle
            tolerance = 5  # Tolerance in degrees
            filtered_vertices = []
            for i, angle in enumerate(angles):
                if abs(angle - avg_angle) <= tolerance:
                    filtered_vertices.append(vertices[i])

            vertices_arr.append(np.array(filtered_vertices))
            lines_arr.append(lines)

        return vertices_arr, lines_arr

    
    def calculate_distance(self, p1, p2):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(p2 - p1)

    def filter_points(self, points):
        print(points)
        distances = [self.calculate_distance(points[i], points[(i+1) % len(points)]) for i in range(len(points))]
        avg_distance = np.mean(distances)
        threshold = 0.85 * avg_distance
        i = 0
        while i < len(points):
            if distances[i] < threshold:
                dist_prev = self.calculate_distance(points[(i-1 + len(points)) % len(points)], points[i])
                dist_next = self.calculate_distance(points[(i+1) % len(points)], points[(i+2) % len(points)])
                
                if dist_prev <= dist_next:
                    points = np.delete(points, i, axis=0)
                else:
                    points = np.delete(points, (i+1) % len(points), axis=0)
                
                distances = [self.calculate_distance(points[j], points[(j+1) % len(points)]) for j in range(len(points))]
            else:
                i += 1
        
        return points

    def calculate_angle(self, point, centroid):
        return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])

    def get_best_fit_polygon(self, vertices, lines):
        centroid = np.mean(vertices, axis=0)
        distances = np.linalg.norm(vertices - centroid, axis=1)
        average_radius = np.mean(distances)
        n_vertices = len(vertices)

        def generate_regular_polygon(centroid, radius, n_vertices, rotation_angle=0):
            angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False) + rotation_angle
            return np.array([
                [centroid[0] + radius * np.cos(angle), centroid[1] + radius * np.sin(angle)]
                for angle in angles
            ])

        def fit_score(vertices, approx_vertices):
            return np.sum(cdist(vertices, approx_vertices, 'euclidean').min(axis=1))

        def line_fit_score(lines, approx_vertices):
            total_distance = 0
            total_samples = 0

            for line in lines:
                p1, p2 = line
                segment_points = self.sample_points_along_segment(p1, p2)
                distances = cdist(segment_points, approx_vertices, 'euclidean').min(axis=1)
                total_distance += np.sum(distances)
                total_samples += len(distances)

            return total_distance / total_samples

        best_fit_polygon = None
        best_fit_score = float('inf')
        best_rotation_angle = 0
        best_radius = average_radius

        radii = np.linspace(average_radius - 1, average_radius + 1, 50)
        for radius in radii:
            for angle in np.linspace(0, 2 * np.pi, 360):
                approx_vertices = generate_regular_polygon(centroid, radius, n_vertices, rotation_angle=angle)
                vertex_score = fit_score(vertices, approx_vertices)
                line_score = line_fit_score(lines, approx_vertices)
                score = vertex_score + line_score
                if score < best_fit_score:
                    best_fit_score = score
                    best_fit_polygon = approx_vertices
                    best_rotation_angle = angle
                    best_radius = radius

        return best_fit_polygon, best_rotation_angle, best_radius

    def process_polygons_with_fit(self, vertices_list, lines_list):
        valid_polygons = []
        rejected_polygons = []
        remaining_segments = []

        for vertices, lines in zip(vertices_list, lines_list):
            if len(vertices) == 0 or len(lines) == 0:
                continue

            best_fit_polygon, best_rotation_angle, best_radius = self.get_best_fit_polygon(vertices, lines)

            line_errors = []
            for line in lines:
                p1, p2 = line
                segment_points = self.sample_points_along_segment(p1, p2)
                distances = cdist(segment_points, best_fit_polygon, 'euclidean').min(axis=1)
                line_errors.append(np.mean(distances))

            if any(error > self.error_threshold for error in line_errors):
                rejected_polygons.append((vertices, lines))
                for line in lines:
                    remaining_segments.append(line)
                continue

            valid_polygons.append((best_fit_polygon, best_rotation_angle, best_radius))

        return valid_polygons, rejected_polygons, remaining_segments

    def handle_remaining_segments(self, remaining_segments):
        heapq.heapify(remaining_segments)
        final_polygons = []
        utilized_segments = set()

        while remaining_segments:
            current_segment = heapq.heappop(remaining_segments)
            if any(tuple(map(tuple, segment)) in utilized_segments for segment in current_segment):
                continue

            remaining_polygons = [segment for segment in current_segment if tuple(map(tuple, segment)) not in utilized_segments]

            if len(remaining_polygons) == 0:
                continue

            vertices = np.array([point for segment in remaining_polygons for point in segment])
            lines = remaining_polygons
            best_fit_polygon, best_rotation_angle, best_radius = self.get_best_fit_polygon(vertices, lines)

            line_errors = []
            for line in lines:
                p1, p2 = line
                segment_points = self.sample_points_along_segment(p1, p2)
                distances = cdist(segment_points, best_fit_polygon, 'euclidean').min(axis=1)
                line_errors.append(np.mean(distances))

            if any(error > self.error_threshold for error in line_errors):
                for line in lines:
                    remaining_segments.append(line)
                continue

            final_polygons.append((best_fit_polygon, best_rotation_angle, best_radius))
            for segment in lines:
                utilized_segments.add(tuple(map(tuple, segment)))

        return final_polygons
