from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from cycle_detection import *
from circle_detection import *
from curve_processing import *
from polygon_detection import *
from segment_processing import *
from svg_processing import *

def run():
    svg_processor = SVGProcessor(svg_file='../data/problems/frag0.svg')
    svg_processor.extract_all_points()

    curves = defaultdict(list)
    for point in svg_processor.all_points:
        curve_index, _, x, y = point
        curves[curve_index].append((x, y))

    curve_processor = CurveProcessor(curves)
    curve_processor.process()
    curves = curve_processor.segment_points_dict

    cycle_detector = CycleDetector(curve_processor.updated_curves)
    cycles, non_cycle_lines = cycle_detector.process_cycles()
    print("Unique Cycles:")
    for cycle in cycles:
        print(cycle)

    print("\nNon-Cycle Lines:")
    for line in non_cycle_lines:
        print(line)

    circle_detector = CircleDetector(cycles)
    remaining_sides = circle_detector.remaining_sides
    filtered_unused_loops, possible_circles = circle_detector.detect_circles()
    print(possible_circles)

    unique_cycles = circle_detector.unique_cycles

    print("Unused Loops:")
    for loop in filtered_unused_loops:
        print(loop)
        
        for polygon in unique_cycles:
            for i in range(len(polygon)):
                side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
                remaining_sides.add(side)

    # Remove sides in possible_circles
    for _, _, polygon in possible_circles:
        for i in range(len(polygon)):
            side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
            if side in remaining_sides:
                remaining_sides.remove(side)

    # Remove sides in filtered_unused_loops
    for polygon in filtered_unused_loops:
        for i in range(len(polygon)):
            side = tuple(sorted([tuple(polygon[i]), tuple(polygon[(i + 1) % len(polygon)])]))
            if side in remaining_sides:
                remaining_sides.remove(side)

    print(remaining_sides)

    segments = list(non_cycle_lines)

    segment_processor = SegmentProcessor(segments)
    segment_processor.merge_collinear_segments()
    segment_processor.find_segments_with_common_vertices()
    rem = segment_processor.revert_to_original_segments()
    segment_processor.filter_merged_segments()

    segment_processor.plot_segments(segment_processor.filtered_merged_segments, "Merged Segments Excluding Common Vertices")
    segment_processor.plot_segments(rem, "Original Segments with Common Vertices")

    remaining_sides = remaining_sides.union(set(rem))
    print(remaining_sides)

    polygon_detection = PolygonDetection()

    # Process the polygons to get vertices and lines
    vertices_arr, lines_arr = polygon_detection.process_polygons(filtered_unused_loops)
    print("Vertices Array:")
    print(vertices_arr)
    print("Lines Array:")
    print(lines_arr)

    # Plot the polygons
    plt.figure(figsize=(10, 10))
    for vertices in vertices_arr:
        if len(vertices) > 0:  # Check if vertices is not empty
            plt.plot(vertices[:, 0], vertices[:, 1], 'o', label='Processed Vertices')

    for lines in lines_arr:
        for line in lines:
            x_values, y_values = zip(*line)
            plt.plot(x_values, y_values, 'k--', alpha=0.5)

    # Plot the original points for reference
    for points in filtered_unused_loops:
        plt.plot([p[0] for p in points], [p[1] for p in points], 'x--', label='Original Points')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Processed and Original Polygons')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Process polygons to find valid and rejected polygons
    valid_polygons, rejected_polygons, remaining_segments = polygon_detection.process_polygons_with_fit(vertices_arr, lines_arr)

    # Handle remaining segments to form final polygons
    final_polygons = polygon_detection.handle_remaining_segments(remaining_segments)

    print("Valid Polygons:")
    print(valid_polygons)

    print("Rejected Polygons:")
    print(rejected_polygons)

    print("Final Polygons from Remaining Segments:")
    print(final_polygons)

    # Plot valid and final polygons
    plt.figure(figsize=(10, 10))
    for best_fit_polygon, best_rotation_angle, best_radius in valid_polygons:
        plt.plot(np.append(best_fit_polygon[:, 0], best_fit_polygon[0, 0]), 
                np.append(best_fit_polygon[:, 1], best_fit_polygon[0, 1]), 'ro-', label='Best Fit Polygon')

    for best_fit_polygon, best_rotation_angle, best_radius in final_polygons:
        plt.plot(np.append(best_fit_polygon[:, 0], best_fit_polygon[0, 0]), 
                np.append(best_fit_polygon[:, 1], best_fit_polygon[0, 1]), 'go-', label='Final Polygon')

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Valid and Final Polygons')
    plt.grid(True)
    plt.show()

    def plot_all(valid_polygons, possible_circles, remaining_sides, curves, inverse_dict, merged_segments):
        plt.figure(figsize=(12, 12))
        remaining_sides = set([
            ((float(x1), float(y1)), (float(x2), float(y2)))
            for ((x1, y1), (x2, y2)) in remaining_sides
        ])

        all_x = []
        all_y = []

        for best_fit_polygon, best_rotation_angle, best_radius in valid_polygons:
            all_x.extend(best_fit_polygon[:, 0])
            all_y.extend(best_fit_polygon[:, 1])
            plt.plot(np.append(best_fit_polygon[:, 0], best_fit_polygon[0, 0]), 
                    np.append(best_fit_polygon[:, 1], best_fit_polygon[0, 1]), 'ro-', label='Best Fit Polygon')

        for center, radius, circle_points in possible_circles:
            circle = plt.Circle(center, radius, color='b', fill=False)
            plt.gca().add_artist(circle)
            all_x.append(center[0] + radius)
            all_x.append(center[0] - radius)
            all_y.append(center[1] + radius)
            all_y.append(center[1] - radius)
            circle_points = np.array(circle_points)
            all_x.extend(circle_points[:, 0])
            all_y.extend(circle_points[:, 1])

        plotted_curves = set()
        
        for side in remaining_sides:
            if side in inverse_dict:
                curve_num = inverse_dict[side]
            elif (side[1], side[0]) in inverse_dict:
                curve_num = inverse_dict[(side[1], side[0])]
            else:
                print(f"Side {side} not found in inverse_dict.")
                continue
            
            if curve_num not in plotted_curves:
                if curve_num in curves:
                    points = curves[curve_num]
                    # Unpack points into x_values and y_values
                    x_values, y_values = zip(*points)
                    all_x.extend(x_values)
                    all_y.extend(y_values)
                    plt.plot(x_values, y_values, label=f'Curve {curve_num}')
                    plotted_curves.add(curve_num)

        for segment in merged_segments:
            (x1, y1), (x2, y2) = segment
            all_x.extend([x1, x2])
            all_y.extend([y1, y2])
            plt.plot([x1, x2], [y1, y2], 'g-', label='Merged Segment')

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Valid Polygons, Possible Circles, Remaining Curves, and Merged Segments')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')  # Ensures the aspect ratio is equal to avoid distortion
        plt.show()

    plot_all(valid_polygons, possible_circles, remaining_sides, curves, curve_processor.inverse_dict, segment_processor.filtered_merged_segments)
    print(remaining_sides)

if __name__ == "__main__":
    run()
    print(1)

