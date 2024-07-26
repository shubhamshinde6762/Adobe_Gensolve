import numpy as np
from svgpathtools import svg2paths
from scipy.special import binom

def extract_bezier_curves(svg_file):
    """
    Extract cubic and quadratic Bezier curves from an SVG file.

    Args:
        svg_file (str): Path to the SVG file.

    Returns:
        tuple: A tuple containing two numpy arrays:
            - cubic_bezier_points: Array of cubic Bezier curves, each represented by control points.
            - quadratic_bezier_points: Array of quadratic Bezier curves, each represented by control points.
    """
    paths, _ = svg2paths(svg_file)
    
    cubic_bezier_points = []
    quadratic_bezier_points = []

    for path in paths:
        for segment in path:
            if segment.__class__.__name__ == 'CubicBezier':
                cubic_bezier_points.append([
                    (segment.start.real, segment.start.imag),
                    (segment.control1.real, segment.control1.imag),
                    (segment.control2.real, segment.control2.imag),
                    (segment.end.real, segment.end.imag)
                ])
            elif segment.__class__.__name__ == 'QuadraticBezier':
                quadratic_bezier_points.append([
                    (segment.start.real, segment.start.imag),
                    (segment.control.real, segment.control.imag),
                    (segment.end.real, segment.end.imag)
                ])
    
    cubic_bezier_points = np.array(cubic_bezier_points)
    quadratic_bezier_points = np.array(quadratic_bezier_points)
    return cubic_bezier_points, quadratic_bezier_points