import math
import heapq
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

class PolygonDetection:
    def __init__(self, error_threshold=150):
        self.error_threshold = error_threshold
        self.polygons = []
        
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

            concave_vertices = []
            for i in range(len(points)):
                p_prev = points[i - 1]
                p_curr = points[i]
                p_next = points[(i + 1) % len(points)]
                angle = self.calculate_internal_angle(p_prev, p_curr, p_next)
                if angle > 180:
                    concave_vertices.append(p_curr)

            points = [p for p in points if p not in concave_vertices]

            points = self.filter_points(np.array(points))
            # print(points)
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
                # print(score, vertex)
                vertex_tuple = tuple(vertex)  # Convert numpy array to a tuple
                if not any(self.are_points_close(vertex, np.array(v)) for v in vertices):
                    vertices.add(vertex_tuple)

            vertices = np.array([np.array(v) for v in vertices])
            vertices_arr.append(vertices)
            lines_arr.append(lines)
        return vertices_arr, lines_arr
    
    def calculate_distance(self, p1, p2):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(p2 - p1)

    def filter_points(self, points):
        # print(points)
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

    def get_best_fit_rectangle(self, vertices, lines):
        if len(vertices) != 4:
            return None, None, None  
        side_lengths = np.array([np.linalg.norm(vertices[i] - vertices[(i+1) % 4]) for i in range(4)])

        if not (np.isclose(side_lengths[0], side_lengths[2], rtol=0.1) and np.isclose(side_lengths[1], side_lengths[3], rtol=0.1)):
            return None, None, None

        min_adjacent_ratio = np.min(side_lengths) / np.max(side_lengths)
        if min_adjacent_ratio > 0.75:
            return None, None, None

        centroid = np.mean(vertices, axis=0)
        
        best_rotation_angle = 0  # Placeholder for rotation calculation

        rectangle_vertices = np.array([
            centroid + np.array([-side_lengths[0] / 2, -side_lengths[1] / 2]),
            centroid + np.array([side_lengths[0] / 2, -side_lengths[1] / 2]),
            centroid + np.array([side_lengths[0] / 2, side_lengths[1] / 2]),
            centroid + np.array([-side_lengths[0] / 2, side_lengths[1] / 2])
        ])

        return rectangle_vertices, best_rotation_angle, None 

    def get_best_fit_star_shape(self, vertices, lines):
        centroid = np.mean(vertices, axis=0)

        distances = np.linalg.norm(vertices - centroid, axis=1)

        angles = np.arctan2(vertices[:, 1] - centroid[1], vertices[:, 0] - centroid[0])
        sorted_indices = np.argsort(angles)
        sorted_vertices = vertices[sorted_indices]

        outer_vertices = sorted_vertices[::2]
        inner_vertices = sorted_vertices[1::2]

        star_points = np.empty((len(vertices), 2))
        star_points[::2] = outer_vertices
        star_points[1::2] = inner_vertices

        best_rotation_angle = 0  
        best_radius = np.mean(distances[sorted_indices[::2]])
        return star_points, best_rotation_angle, best_radius


    def process_polygons_with_fit(self, vertices_list, lines_list):
        valid_polygons = []
        rejected_polygons = []
        remaining_segments = []

        for vertices, lines in zip(vertices_list, lines_list):
            best_fit_polygon, best_rotation_angle, best_radius = None, None, None
            if len(vertices) == 0 or len(lines) == 0:
                continue

            polygon_type = "polygon"

            if len(vertices) % 2 == 0 and len(vertices) >= 8:
                best_fit_polygon, best_rotation_angle, best_radius = self.get_best_fit_star_shape(vertices, lines)
                if best_fit_polygon is None:
                    best_fit_polygon, best_rotation_angle, best_radius = self.get_best_fit_polygon(vertices, lines)
                else:
                    polygon_type = "star"
                    
            elif len(vertices) == 4:
                best_fit_polygon, best_rotation_angle, _ = self.get_best_fit_rectangle(vertices, lines)
                if best_fit_polygon is not None:
                    polygon_type = "rectangle"
                else:
                    best_fit_polygon, best_rotation_angle, best_radius = self.get_best_fit_polygon(vertices, lines)

            else:
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

            # Store the valid polygon with its type
            valid_polygons.append((best_fit_polygon, best_rotation_angle, best_radius, polygon_type))

        self.polygons = valid_polygons  # Store the valid polygons
        return valid_polygons, rejected_polygons, remaining_segments

    def plot_all_polygons_with_symmetry(self):
        """
        Plot all the stored polygons along with their lines of symmetry.
        """
        for polygon_data in self.polygons:
            polygon_vertices, rotation_angle, radius, polygon_type = polygon_data
            self.plot_lines_of_symmetry(polygon_vertices, polygon_type=polygon_type)

    def plot_lines_of_symmetry(self, polygon_vertices, polygon_type="polygon"):
        """
        Plot lines of symmetry for regular polygons and rectangles.

        :param polygon_vertices: Array of vertices for the polygon/rectangle.
        :param polygon_type: Type of polygon, either "polygon" or "rectangle".
        """
        centroid = np.mean(polygon_vertices, axis=0)
        
        plt.figure(figsize=(6, 6))
        plt.plot(*polygon_vertices.T, 'r-', label='Polygon')
        plt.plot([polygon_vertices[-1, 0], polygon_vertices[0, 0]],
                [polygon_vertices[-1, 1], polygon_vertices[0, 1]], 'r-')

        # Plot centroid
        plt.plot(centroid[0], centroid[1], 'ro', label='Centroid')

        if polygon_type == "polygon" or polygon_type == "star":
            for vertex in polygon_vertices:
                plt.plot([vertex[0], centroid[0]], [vertex[1], centroid[1]], 'g--', label='Line of Symmetry')

            if len(polygon_vertices) % 2 == 0 and polygon_type == "polygon":
                num_vertices = len(polygon_vertices)
                for i in range(num_vertices // 2):
                    opposite_vertex = polygon_vertices[(i + num_vertices // 2) % num_vertices]
                    plt.plot([polygon_vertices[i][0], opposite_vertex[0]],
                            [polygon_vertices[i][1], opposite_vertex[1]], 'g--', label='Line of Symmetry')

                for i in range(num_vertices):
                    next_i = (i + 1) % num_vertices
                    midpoint = (polygon_vertices[i] + polygon_vertices[next_i]) / 2
                    opposite_midpoint = (polygon_vertices[(i + num_vertices // 2) % num_vertices] +
                                        polygon_vertices[(next_i + num_vertices // 2) % num_vertices]) / 2
                    plt.plot([midpoint[0], opposite_midpoint[0]], [midpoint[1], opposite_midpoint[1]], 'g--', label='Line of Symmetry')

        elif polygon_type == "rectangle":
            diagonals = [
                (polygon_vertices[0], polygon_vertices[2]),
                (polygon_vertices[1], polygon_vertices[3])
            ]
            for diagonal in diagonals:
                plt.plot([diagonal[0][0], diagonal[1][0]], [diagonal[0][1], diagonal[1][1]], 'g--', label='Diagonal')

            for i in range(2):
                midpoint = (polygon_vertices[i] + polygon_vertices[(i+2) % 4]) / 2
                plt.plot([midpoint[0], centroid[0]], [midpoint[1], centroid[1]], 'b--', label='Midline')
        
        plt.axis('equal')
        plt.legend()
        plt.title('Lines of Symmetry')
        plt.show()


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
