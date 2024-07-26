import numpy as np
from svgpathtools import svg2paths
from scipy.special import binom

def bernstein_poly(i, n, t):
    """
    Calculate the Bernstein polynomial.

    Args:
        i (int): The index of the polynomial.
        n (int): The degree of the polynomial.
        t (numpy.ndarray): The parameter values.

    Returns:
        numpy.ndarray: The evaluated Bernstein polynomial.
    """
    return binom(n, i) * (t**(n-i)) * ((1 - t)**i)




def bezier_curve(points, n_points=100):
    """
    Compute the Bézier curve from a set of control points.

    Args:
        points (numpy.ndarray): Control points for the Bézier curve.
        n_points (int): Number of points to sample along the curve.

    Returns:
        numpy.ndarray: The points of the Bézier curve.
    """
    n = len(points) - 1
    t = np.linspace(0, 1, n_points)
    curve = np.zeros((n_points, 2))
    for i in range(n + 1):
        curve += np.outer(bernstein_poly(i, n, t), points[i])
    return curve




def bezier_derivatives(points, n_points=100):
    """
    Compute the first and second derivatives of the Bézier curve.

    Args:
        points (numpy.ndarray): Control points for the Bézier curve.
        n_points (int): Number of points to sample along the curve.

    Returns:
        tuple: A tuple containing two numpy arrays:
            - d_curve: The first derivative of the Bézier curve.
            - d2_curve: The second derivative of the Bézier curve.
    """
    n = len(points) - 1
    t = np.linspace(0, 1, n_points)
    d_curve = np.zeros((n_points, 2))
    d2_curve = np.zeros((n_points, 2))
    
    for i in range(n):
        d_curve += np.outer(bernstein_poly(i, n-1, t), n * (points[i+1] - points[i]))
    
    for i in range(n-1):
        d2_curve += np.outer(bernstein_poly(i, n-2, t), n * (n-1) * (points[i+2] - 2*points[i+1] + points[i]))
    
    return d_curve, d2_curve