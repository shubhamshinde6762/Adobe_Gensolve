import numpy as np
from svgpathtools import svg2paths
from scipy.special import binom
from .core import bezier_curve, bezier_derivatives

def osculating_circle_center(points, threshold, n_points=100):
    """
    Compute the centers of osculating circles for a Bézier curve and filter by threshold.

    Args:
        points (numpy.ndarray): Control points for the Bézier curve.
        threshold (float): Distance threshold for considering osculating circle centers.
        n_points (int): Number of points to sample along the curve.

    Returns:
        numpy.ndarray: The centers of osculating circles within the threshold distance.
    """
    curve = bezier_curve(points, n_points)
    d_curve, d2_curve = bezier_derivatives(points, n_points)
    
    curvature = (d_curve[:, 0] * d2_curve[:, 1] - d_curve[:, 1] * d2_curve[:, 0]) / (d_curve[:, 0]**2 + d_curve[:, 1]**2)**1.5
    radius_of_curvature = 1 / np.abs(curvature)
    
    normal = np.zeros_like(d_curve)
    normal[:, 0] = -d_curve[:, 1]
    normal[:, 1] = d_curve[:, 0]
    normal_direction = np.sign(curvature)
    normal *= normal_direction[:, np.newaxis]
    normal /= np.linalg.norm(normal, axis=1, keepdims=True)
    
    centers = curve + normal * radius_of_curvature[:, np.newaxis]
    
    # Filter centers based on threshold distance from the curve
    distances = np.linalg.norm(centers - curve, axis=1)
    valid_centers = centers[distances < threshold]
    
    return valid_centers




def calculate_curvature(points, n_points=100):
    """
    Calculate the curvature of a Bézier curve.

    Args:
        points (numpy.ndarray): Control points for the Bézier curve.
        n_points (int): Number of points to sample along the curve.

    Returns:
        numpy.ndarray: The curvature values of the Bézier curve.
    """
    curve = bezier_curve(points, n_points)
    d_curve, d2_curve = bezier_derivatives(points, n_points)
    
    curvature = (d_curve[:, 0] * d2_curve[:, 1] - d_curve[:, 1] * d2_curve[:, 0]) / (d_curve[:, 0]**2 + d_curve[:, 1]**2)**1.5
    return curvature