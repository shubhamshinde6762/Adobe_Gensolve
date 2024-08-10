from utils.cycle_detection import *
from utils.circle_detection import *
from utils.curve_processing import *
from utils.polygon_detection import *
from utils.segment_processing import *
from utils.svg_processing import *
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import csv
from io import StringIO 

def process_csv_data(csv_data: str):
    # Initialize SVGProcessor with CSV data
    svg_processor = SVGProcessor(csv_data)
    svg_processor.extract_points_from_csv()

    curves = defaultdict(list)
    for point in svg_processor.all_points:
        curve_index, _, x, y = point
        curves[curve_index].append((x, y))

    curve_processor = CurveProcessor(curves)
    curve_processor.process()
    curves = curve_processor.segment_points_dict

    cycle_detector = CycleDetector(curve_processor.updated_curves)
    cycles, non_cycle_lines = cycle_detector.process_cycles()

    circle_detector = CircleDetector(cycles)
    remaining_sides = circle_detector.remaining_sides
    filtered_unused_loops, possible_circles = circle_detector.detect_circles()

    unique_cycles = circle_detector.unique_cycles

    for polygon in unique_cycles:
        for i in range(len(polygon)):
            side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
            remaining_sides.add(side)

    for _, _, polygon in possible_circles:
        for i in range(len(polygon)):
            side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
            if side in remaining_sides:
                remaining_sides.remove(side)

    for polygon in filtered_unused_loops:
        for i in range(len(polygon)):
            side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
            if side in remaining_sides:
                remaining_sides.remove(side)

    segments = list(non_cycle_lines)

    segment_processor = SegmentProcessor(segments)
    segment_processor.merge_collinear_segments()
    segment_processor.find_segments_with_common_vertices()
    rem = segment_processor.revert_to_original_segments()
    segment_processor.filter_merged_segments()
    remaining_sides = remaining_sides.union(set(rem))

    polygon_detection = PolygonDetection()
    vertices_arr, lines_arr = polygon_detection.process_polygons(filtered_unused_loops)

    valid_polygons, rejected_polygons, remaining_segments = polygon_detection.process_polygons_with_fit(vertices_arr, lines_arr)

    def interpolate_points(p1, p2, num_points=5):
        x_values = np.linspace(p1[0], p2[0], num_points)
        y_values = np.linspace(p1[1], p2[1], num_points)
        return list(zip(x_values, y_values))

    def generate_circle_points(center, radius, num_points):
        theta = np.linspace(0, 2 * np.pi, num_points)
        x_values = center[0] + radius * np.cos(theta)
        y_values = center[1] + radius * np.sin(theta)
        return list(zip(x_values, y_values))

    def convert_points_to_csv(valid_polygons, possible_circles, remaining_sides, curves, inverse_dict, merged_segments):
        data = []
        index = 0  # Starting index

        # Process valid polygons
        for idx, (best_fit_polygon, best_rotation_angle, best_radius) in enumerate(valid_polygons):
            num_points = best_fit_polygon.shape[0]
            for i in range(num_points):
                p1 = best_fit_polygon[i]
                p2 = best_fit_polygon[(i + 1) % num_points]
                interpolated_points = interpolate_points(p1, p2)
                for point in interpolated_points:
                    data.append([index, '0.0000', point[0], point[1]])
            index += 1

        # Process possible circles
        for idx, (center, radius, circle_points) in enumerate(possible_circles):
            num_circle_points = int(10)
            circle_points = generate_circle_points(center, radius, num_circle_points)
            for point in circle_points:
                data.append([index, '0.0000', point[0], point[1]])
            index += 1

        # Process remaining sides
        plotted_curves = set()
        for side in remaining_sides:
            if side in inverse_dict:
                curve_num = inverse_dict[side]
            elif (side[1], side[0]) in inverse_dict:
                curve_num = inverse_dict[(side[1], side[0])]
            else:
                continue

            if curve_num not in plotted_curves:
                if curve_num in curves:
                    points = curves[curve_num]
                    for i in range(len(points) - 1):
                        p1 = points[i]
                        p2 = points[i + 1]
                        interpolated_points = interpolate_points(p1, p2)
                        for point in interpolated_points:
                            data.append([index, '0.0000', point[0], point[1]])
                    plotted_curves.add(curve_num)
                    index += 1

        # Process merged segments
        for idx, segment in enumerate(merged_segments):
            p1, p2 = segment
            interpolated_points = interpolate_points(p1, p2)
            for point in interpolated_points:
                data.append([index, '0.0000', point[0], point[1]])
            index += 1

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['CurveIndex', 'Static', 'X', 'Y'])
        writer.writerows(data)
        return output.getvalue()

    csv_result = convert_points_to_csv(valid_polygons, possible_circles, remaining_sides, curves, curve_processor.inverse_dict, segment_processor.filtered_merged_segments)
    return csv_result

