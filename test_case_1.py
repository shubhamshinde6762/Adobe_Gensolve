from bezier_utils.basic import extract_bezier_curves
from bezier_utils.linearity import is_approximately_linear_by_curvature
from bezier_utils.square_approx import draw_quadrilateral_with_square, get_quadrilateral_and_square_vertices
from bezier_utils.display import plot_bezier_curve_cubic
from bezier_utils.circle_approx import process_bezier_and_circles
import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
from geomutils.core import mediate_points, mediate_lines, create_polygon_lines, calculate_angle, remove_elements
from geomutils.display import plot_polygon, plot_arrows_between_points
from geomutils.polygons import order_points_clockwise, build_connection_map, get_all_points, remove_finder
from matplotlib.path import Path
import matplotlib.patches as patches

c, looped, circle_fits = process_bezier_and_circles(extract_bezier_curves('data/problems/frag0.svg')[0])
lines = []
unprocessed_beziers = []
for curve in c:
    if is_approximately_linear_by_curvature(curve, tolerance=0.01):
        lines.append(np.array([curve[0], curve[-1]]))
    else:
        unprocessed_beziers.append(curve)

unmediated_points = []
for line in lines:
    unmediated_points.append(line[0])
    unmediated_points.append(line[1])
mediated_points = mediate_points(unmediated_points, 0.5)
mediated_lines = mediate_lines(lines, mediated_points)
connections = build_connection_map(mediated_lines)
points = get_all_points(mediated_lines)
ordered_points = order_points_clockwise(points, connections)
remove_vertices = remove_finder(ordered_points)

flattened_ordered_points = remove_elements(ordered_points, remove_vertices)
flattened_polygon = create_polygon_lines(flattened_ordered_points)
square_vertices = get_quadrilateral_and_square_vertices(flattened_polygon)

circle = circle_fits[0]
fig, ax = plt.subplots()
for control_points in unprocessed_beziers:
    plot_bezier_curve_cubic(ax, control_points)
square_path = Path(square_vertices + [square_vertices[0]], closed=True)
patch = patches.PathPatch(square_path, facecolor='none', edgecolor='green')
ax.add_patch(patch)
circle_patch = patches.Circle((circle[0], circle[1]), circle[2], edgecolor='red', facecolor='none')
ax.add_patch(circle_patch)
ax.set_xlim(-10, 240)
ax.set_ylim(-10, 240)
ax.set_aspect('equal', 'box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Bezier Curves, Square, and Circle')
plt.grid(True)
plt.show()