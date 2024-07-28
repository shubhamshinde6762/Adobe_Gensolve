from scipy.spatial.distance import euclidean 
import numpy as np

def points_close(point_1, point_2, threshold):
    """
    Check if two points are within a specified distance threshold and return their midpoint if they are.

    Parameters:
    point_1 (array-like): The first point, typically an array or list of coordinates [x, y, ...].
    point_2 (array-like): The second point, typically an array or list of coordinates [x, y, ...].
    threshold (float): The maximum allowable distance between the two points to consider them close.

    Returns:
    numpy.ndarray or None: The midpoint of the two points as a numpy array if their distance is within the threshold, otherwise None.

    Example:
    >>> import numpy as np
    >>> point_1 = np.array([1.0, 2.0])
    >>> point_2 = np.array([2.0, 3.0])
    >>> threshold = 1.5
    >>> points_close(point_1, point_2, threshold)
    array([1.5, 2.5])
    """
    import numpy as np
    from scipy.spatial.distance import euclidean

    # Calculate the Euclidean distance between the two points
    dist = euclidean(point_1, point_2)

    # Check if the distance is within the specified threshold
    if dist <= threshold:
        # Return the midpoint of the two points
        return (point_1 + point_2) / 2
    else:
        # Return None if the points are not close enough
        return None




def mediate_points(points, threshold):
    """
    Find and return the list of midpoints for pairs of points that are within a specified distance threshold.

    Parameters:
    points (list of array-like): A list of points, each typically an array or list of coordinates [x, y, ...].
    threshold (float): The maximum allowable distance between pairs of points to consider them close.

    Returns:
    list of numpy.ndarray: A list of midpoints of pairs of points that are within the threshold distance.

    Example:
    >>> import numpy as np
    >>> points = [np.array([1.0, 2.0]), np.array([2.0, 3.0]), np.array([10.0, 10.0])]
    >>> threshold = 1.5
    >>> mediate_points(points, threshold)
    [array([1.5, 2.5])]
    """
    mediated_points = []
    for i in range(0, len(points)):
        for j in range(i + 1, len(points)):
            if np.any(points_close(points[i], points[j], threshold)) != None:
                mediated_points.append(points_close(points[i], points[j], threshold))
    return mediated_points




def mediate_lines(lines, mediated_points):
    """
    Adjusts the endpoints of line segments based on proximity to a set of mediated points.

    This function iterates through a list of line segments and updates their endpoints 
    to the nearest mediated point if the distance between the endpoint and a mediated 
    point is less than or equal to a specified threshold (0.5 units). The updated line 
    segments are then returned.

    Parameters:
    - lines (list of np.ndarray): A list of line segments, where each line segment is 
      represented as a 2x2 numpy array with two points (start and end).
    - mediated_points (list of np.ndarray): A list of points to which the line segment 
      endpoints are compared.

    Returns:
    - list of np.ndarray: A list of updated line segments, where each line segment is 
      represented as a 2x2 numpy array with updated endpoints.
    """
    mediated_lines = []
    for line in lines:
        first_point = line[0]
        second_point = line[1]
        for mediated_point in mediated_points:
            if euclidean(first_point, mediated_point) <= 0.5:
                first_point = mediated_point
            if euclidean(second_point, mediated_point) <= 0.5:
                second_point = mediated_point
        mediated_lines.append(np.vstack((first_point, second_point)))
    return mediated_lines




def create_polygon_lines(points):
    """
    Create a list of lines from an ordered list of points that constitute a closed polygon.
    
    Each point is represented as a numpy array of length 2. Each line is represented as a 
    numpy array containing the two endpoints of that line.
    
    Parameters:
    points (list of numpy arrays): An ordered list of points, where each point is a numpy array 
                                   of length 2. The list should contain at least 3 points.
    
    Returns:
    list of numpy arrays: A list of lines, where each line is represented as a numpy array 
                          containing the two endpoints of that line.
                          
    Example:
    >>> points = [np.array([0, 0]), np.array([1, 0]), np.array([1, 1]), np.array([0, 1])]
    >>> lines = create_polygon_lines(points)
    >>> for line in lines:
    >>>     print(line)
    [[0 0]
     [1 0]]
    [[1 0]
     [1 1]]
    [[1 1]
     [0 1]]
    [[0 1]
     [0 0]]
    """
    lines = []
    num_points = len(points)
    
    for i in range(num_points):
        start_point = points[i]
        end_point = points[(i + 1) % num_points]  # Wrap around to the first point for the last line
        line = np.array([start_point, end_point])
        lines.append(line)
    
    return lines




def calculate_angle(a, b, c):
    """ Calculate the angle at vertex b with points a, b, c """
    ab = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cos_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle = np.degrees(angle)
    if angle>180:
        angle = 360-angle
    return angle




def remove_elements(list1, list2):
    set2 = set(list2)
    result = [item for item in list1 if item not in set2]
    return result