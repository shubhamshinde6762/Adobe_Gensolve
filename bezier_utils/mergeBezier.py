import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.special import comb

def bernstein_poly(i, n, t):
    return comb(n, i) * (t**i) * ((1 - t)**(n - i))

def bezier_curve(control_points, num_points=300):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, control_points.shape[1]))

    for i in range(n + 1):
        curve_points += bernstein_poly(i, n, t)[:, np.newaxis] * control_points[i]
    
    return curve_points

def line_equation(p1, p2):
    A = p2[1] - p1[1]
    B = p1[0] - p2[0]
    C = A * p1[0] + B * p1[1]
    return A, B, -C

def point_line_distance(point, line):
    A, B, C = line
    return abs(A * point[0] + B * point[1] + C) / np.sqrt(A**2 + B**2)

def angle_between_lines(line1, line2):
    """Calculate the angle between two lines."""
    A1, B1, _ = line1
    A2, B2, _ = line2
    dot_product = A1 * A2 + B1 * B2
    norm1 = np.sqrt(A1**2 + B1**2)
    norm2 = np.sqrt(A2**2 + B2**2)
    cos_theta = dot_product / (norm1 * norm2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  
    return np.degrees(angle)

def are_orthogonal(curve1, curve2, angle_threshold=85):
    start1, end1 = curve1[0], curve1[-1]
    start2, end2 = curve2[0], curve2[-1]
    
    line1 = line_equation(start1, end1)
    line2 = line_equation(start2, end2)
    
    angle = angle_between_lines(line1, line2)
    
    return abs(angle - 90) < (90 - angle_threshold)

def are_collinear(curve1, curve2, tolerance=1e-2):
    start1, end1 = curve1[0], curve1[-1]
    start2, end2 = curve2[0], curve2[-1]
    
    line1 = line_equation(start1, end1)
    line2 = line_equation(start2, end2)
    
    distance1 = point_line_distance(start2, line1)
    distance2 = point_line_distance(end2, line1)
    
    return distance1 < tolerance and distance2 < tolerance

def merge_beziers(beziers, proximity_threshold=15, collinearity_tolerance=0.8, orthogonality_threshold=10):
    merged_beziers = []
    remaining_beziers = []
    used = np.zeros(len(beziers), dtype=bool)

    for i in range(len(beziers)):
        # if used[i]:
        #     continue
        
        curve = beziers[i]
        used[i] = True
        merged = False
        
        for j in range(i + 1, len(beziers)):
            # if used[j]:
            #     continue
            
            other_curve = beziers[j]
            dist = np.min([euclidean(curve[-1], other_curve[0]), euclidean(curve[0], other_curve[-1])])
            
            if not are_orthogonal(curve, other_curve, orthogonality_threshold) and \
               (dist < proximity_threshold or are_collinear(curve, other_curve, collinearity_tolerance)):
                curve = np.vstack((curve, other_curve))
                used[j] = True
                merged = True
        
        if merged:
            merged_beziers.append(curve)
        else:
            remaining_beziers.append(curve)
    
    return merged_beziers, remaining_beziers

def plot_beziers(merged_beziers, remaining_beziers, original_beziers):
    plt.figure(figsize=(12, 12))
    
    # print(len(merged_beziers))
    
    for curve in merged_beziers:
        points = bezier_curve(curve)
        plt.plot(points[:, 0], points[:, 1], linestyle='-', color='blue')
    
    print(merged_beziers)
    for curve in remaining_beziers:
        points = bezier_curve(curve)
        plt.plot(points[:, 0], points[:, 1], linestyle='-', color='red')
    
    # original_curves_set = set(tuple(map(tuple, curve)) for curve in original_beziers)
    # for curve in original_beziers:
    #     if tuple(map(tuple, curve)) in original_curves_set:
    #         points = bezier_curve(curve)
    #         plt.plot(points[:, 0], points[:, 1], linestyle=':', color='green')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Merged, Remaining, and Original Bézier Curves')
    plt.grid(True)
    plt.legend()
    plt.show()

