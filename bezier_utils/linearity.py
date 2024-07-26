import numpy as np
from svgpathtools import svg2paths
from scipy.special import binom
from .attributes import calculate_curvature

def is_approximately_linear(curve, tolerance):
    """
    Check if a Bézier curve is approximately linear based on deviation from a straight line.

    Args:
        curve (numpy.ndarray): Points of the Bézier curve.
        tolerance (float): Deviation threshold relative to the length of the line segment.

    Returns:
        bool: True if the curve is approximately linear, False otherwise.
    """
    start_point = curve[0]
    end_point = curve[-1]
    
    # Calculate the line segment length
    line_vector = end_point - start_point
    line_length = np.linalg.norm(line_vector)
    
    # Normalize the line vector
    line_vector /= line_length
    
    # Calculate distances of curve points from the line
    distances = np.abs(np.cross(curve - start_point, line_vector))
    
    # Calculate the maximum deviation
    max_deviation = np.max(distances)
    
    # Normalize the maximum deviation relative to the line length
    normalized_deviation = max_deviation / line_length
    
    # Check if the normalized deviation is below the tolerance
    return normalized_deviation < tolerance




def is_approximately_linear_by_curvature(curve, tolerance):
    """
    Check if a Bézier curve is approximately linear based on curvature.

    Args:
        curve (numpy.ndarray): Points of the Bézier curve.
        tolerance (float): Maximum allowable curvature to consider the curve as approximately linear.

    Returns:
        bool: True if the maximum curvature is below the tolerance, indicating that the curve is approximately linear.
    """
    curvature = calculate_curvature(curve)
    max_curvature = np.max(np.abs(curvature))
    return max_curvature < tolerance