import numpy as np
from .core import calculate_angle

def is_closed_polygon(lines):
    """
    Determines if a set of line segments forms a closed polygon.

    This function analyzes a list of line segments to determine if they form a closed
    polygon. A closed polygon is defined as a shape where each point is connected to exactly 
    two other points, forming a continuous loop without any intersections or missing connections.

    Parameters:
    - lines (list of np.ndarray): A list of line segments, where each line segment is represented
      as a 2x2 numpy array with coordinates of the two endpoints.

    Returns:
    - bool: Returns True if the line segments form a closed polygon, otherwise False.
    """
    # Create a dictionary to track connections
    connections = {}
    
    for line in lines:
        start = tuple(line[0])
        end = tuple(line[1])
        
        if start not in connections:
            connections[start] = []
        if end not in connections:
            connections[end] = []
        
        connections[start].append(end)
        connections[end].append(start)
    
    # Start from an arbitrary point and traverse
    start_point = next(iter(connections))
    visited = set()
    
    def traverse(point, prev_point):
        visited.add(point)
        for neighbor in connections[point]:
            if neighbor != prev_point:
                if neighbor in visited:
                    continue
                traverse(neighbor, point)
    
    traverse(start_point, None)
    
    # Check if we visited all points exactly once and returned to the start point
    return len(visited) == len(connections) and all(len(neighbors) == 2 for neighbors in connections.values())




def get_all_points(lines):
    """
    Extracts all unique points from a list of line segments.

    This function iterates through a list of line segments and collects all unique points
    that are endpoints of the segments.

    Parameters:
    - lines (list of np.ndarray): A list of line segments, where each segment is represented
      as a 2x2 numpy array with coordinates of the two endpoints.

    Returns:
    - list of tuple: A list of unique points, each represented as a tuple of coordinates (x, y).
    """
    points = set()
    for line in lines:
        points.add(tuple(line[0]))
        points.add(tuple(line[1]))
    return list(points)




def build_connection_map(lines):
    """
    Constructs a map of point connections from a list of line segments.

    This function creates a dictionary where each key is a point, and the value is a list of 
    points to which it is connected by line segments.

    Parameters:
    - lines (list of np.ndarray): A list of line segments, where each segment is represented
      as a 2x2 numpy array with coordinates of the two endpoints.

    Returns:
    - dict: A dictionary where keys are points (tuples of coordinates) and values are lists
      of points connected to the key point.
    """
    connections = {}
    for line in lines:
        start = tuple(line[0])
        end = tuple(line[1])
        
        if start not in connections:
            connections[start] = []
        if end not in connections:
            connections[end] = []
        
        connections[start].append(end)
        connections[end].append(start)
    
    return connections




def find_next_point(current_point, prev_point, connections):
    """
    Finds the next point in the sequence given the current point and the previous point.

    This function determines the next point to visit in a sequence, ensuring it is not the 
    previous point.

    Parameters:
    - current_point (tuple): The current point in the sequence, represented as (x, y).
    - prev_point (tuple): The previous point in the sequence, represented as (x, y).
    - connections (dict): A dictionary where keys are points and values are lists of connected points.

    Returns:
    - tuple or None: The next point in the sequence if found, otherwise None.
    """
    for neighbor in connections[current_point]:
        if neighbor != prev_point:
            return neighbor
    return None




def order_points_clockwise(points, connections):
    """
    Orders a list of points to form a closed polygon in a clockwise direction.

    This function starts from an arbitrary point and traverses through connected points
    to order them in a sequence that forms a closed polygon.

    Parameters:
    - points (list of tuple): A list of unique points to be ordered, each represented as (x, y).
    - connections (dict): A dictionary where keys are points and values are lists of connected points.

    Returns:
    - list of tuple: An ordered list of points forming a closed polygon.
    
    Raises:
    - ValueError: If it is not possible to find a valid next point in the sequence.
    """
    # Start from an arbitrary point
    start_point = points[0]
    ordered_points = [start_point]
    
    current_point = start_point
    prev_point = None
    
    while len(ordered_points) < len(points):
        next_point = find_next_point(current_point, prev_point, connections)
        if next_point is None:
            raise ValueError("Could not find a valid next point.")
        ordered_points.append(next_point)
        prev_point = current_point
        current_point = next_point
    
    return ordered_points




def remove_finder(ordered_points):
    """
    Identify and return the vertices of a polygon that should be removed based on an angle criterion.
    
    This function iterates through the vertices of a closed polygon defined by an ordered list of points.
    If the angle formed by three consecutive vertices is greater than or equal to 170 degrees, 
    the middle vertex is added to the list of vertices to be removed.
    
    Parameters:
    ordered_points (list of numpy arrays): An ordered list of points, where each point is a numpy array 
                                           of length 2. The list should contain at least 3 points to form a polygon.
    
    Returns:
    list of numpy arrays: A list of vertices that should be removed based on the angle criterion.
                          
    Example:
    >>> points = [np.array([0, 0]), np.array([1, 0]), np.array([2, 0]), np.array([3, 1]), np.array([4, 0])]
    >>> remove_vertices = remove_finder(points)
    >>> for vertex in remove_vertices:
    >>>     print(vertex)
    [1 0]
    [2 0]
    
    Note:
    The function assumes the existence of a helper function `calculate_angle(point1, point2, point3)` 
    that calculates the angle between the segments formed by (point1, point2) and (point2, point3).
    """
    remove_vertices = []
    a = 0
    b = 1
    c = 2
    while(c != 0):
        if calculate_angle(ordered_points[a], ordered_points[b], ordered_points[c]) >= 170:
            remove_vertices.append(ordered_points[b])
        a += 1
        a %= len(ordered_points)
        b += 1
        b %= len(ordered_points)
        c += 1
        c %= len(ordered_points)
    return remove_vertices
