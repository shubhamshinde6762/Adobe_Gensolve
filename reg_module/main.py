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
    svg_processor = SVGProcessor(svg_file=r"C:\Data\Projects\Adobe_Gensolve\data\problems\frag2.svg")
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

    def interpolate_points(p1, p2, num_points=10):
        """Interpolate points between two points p1 and p2."""
        x_values = np.linspace(p1[0], p2[0], num_points)
        y_values = np.linspace(p1[1], p2[1], num_points)
        return list(zip(x_values, y_values))

    def generate_circle_points(center, radius, num_points):
        """Generate points on a circle given its center and radius."""
        theta = np.linspace(0, 2 * np.pi, num_points)
        x_values = center[0] + radius * np.cos(theta)
        y_values = center[1] + radius * np.sin(theta)
        return list(zip(x_values, y_values))

    def convert_points_to_csv(valid_polygons, possible_circles, remaining_sides, curves, inverse_dict, merged_segments, output_filename):
        data = []
        index = 0  # Starting index

        # Process valid polygons
        for idx, (best_fit_polygon, best_rotation_angle, best_radius) in enumerate(valid_polygons):
            num_points = best_fit_polygon.shape[0]
            for i in range(num_points):
                p1 = best_fit_polygon[i]
                p2 = best_fit_polygon[(i + 1) % num_points]  # wrap around to the first point
                interpolated_points = interpolate_points(p1, p2)
                for point in interpolated_points:
                    data.append([index, '0.0000', point[0], point[1]])
            index += 1

        # Process possible circles
        for idx, (center, radius, circle_points) in enumerate(possible_circles):
            num_circle_points = int(100 * radius)
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

        # Write to CSV file
        with open(output_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Curve Index', 'Static', 'X', 'Y'])
            writer.writerows(data)

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

        # print(possible_circles)
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
        plt.axis('equal') 
        plt.show()

    plot_all(valid_polygons, possible_circles, remaining_sides, curves, curve_processor.inverse_dict, segment_processor.filtered_merged_segments)
    convert_points_to_csv(valid_polygons, possible_circles, remaining_sides, curves, curve_processor.inverse_dict, segment_processor.filtered_merged_segments, "output.csv")
    # print(remaining_sides)

if __name__ == "__main__":
    run()
    # print(1)

