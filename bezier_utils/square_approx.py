import numpy as np
import matplotlib.pyplot as plt

def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def calculate_angle(point1, point2, point3):
    v1 = point1 - point2
    v2 = point3 - point2
    angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
    return angle

def is_roughly_square(quadrilateral, angle_tolerance=0.1, length_tolerance=0.1):
    side_lengths = [calculate_distance(segment[0], segment[1]) for segment in quadrilateral]
    angles = [
        calculate_angle(quadrilateral[0][0], quadrilateral[0][1], quadrilateral[1][1]),
        calculate_angle(quadrilateral[1][0], quadrilateral[1][1], quadrilateral[2][1]),
        calculate_angle(quadrilateral[2][0], quadrilateral[2][1], quadrilateral[3][1]),
        calculate_angle(quadrilateral[3][0], quadrilateral[3][1], quadrilateral[0][1])
    ]
    
    avg_length = np.mean(side_lengths)
    avg_angle = 90
    
    lengths_close = all(abs(length - avg_length) / avg_length < length_tolerance for length in side_lengths)
    angles_close = all(abs(angle - avg_angle) < angle_tolerance * avg_angle for angle in angles)
    
    return lengths_close and angles_close

def draw_quadrilateral_with_square(quadrilateral, a_t=0.1, l_t=0.1):
    fig, ax = plt.subplots()
    
    # Draw the original quadrilateral
    for segment in quadrilateral:
        ax.plot([segment[0][0], segment[1][0]], [segment[0][1], segment[1][1]], 'b-')
    
    if is_roughly_square(quadrilateral, a_t, l_t):
        # Calculate the center of the quadrilateral
        center = np.mean([point for segment in quadrilateral for point in segment], axis=0)
        
        # Calculate the side length of the approximated square
        side_length = np.mean([calculate_distance(segment[0], segment[1]) for segment in quadrilateral])
        
        # Calculate the coordinates of the square's vertices
        half_side = side_length / 2
        square_vertices = [
            center + np.array([-half_side, -half_side]),
            center + np.array([half_side, -half_side]),
            center + np.array([half_side, half_side]),
            center + np.array([-half_side, half_side])
        ]
        
        # Draw the approximated square with dotted lines
        for i in range(4):
            next_i = (i + 1) % 4
            ax.plot(
                [square_vertices[i][0], square_vertices[next_i][0]], 
                [square_vertices[i][1], square_vertices[next_i][1]], 'r--'
            )
    
    ax.set_aspect('equal', adjustable='box')
    plt.show()
