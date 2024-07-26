import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

def bezier_curve_cubic(p0, p1, p2, p3, t):
    """
    Computes a point on a cubic Bezier curve.

    Parameters:
    p0, p1, p2, p3: tuple
        Control points of the Bezier curve.
    t: float
        Parameter between 0 and 1.

    Returns:
    np.array
        The point on the Bezier curve corresponding to the parameter t.
    """
    return (1 - t)**3 * np.array(p0) + 3 * (1 - t)**2 * t * np.array(p1) + 3 * (1 - t) * t**2 * np.array(p2) + t**3 * np.array(p3)

def points_match(p1, p2, tolerance=1e-6):
    """
    Checks if two points match within a given tolerance.

    Parameters:
    p1, p2: tuple
        The points to compare.
    tolerance: float
        The tolerance for comparison.

    Returns:
    bool
        True if the points match within the tolerance, False otherwise.
    """
    return np.linalg.norm(np.array(p1) - np.array(p2)) < tolerance

def find_loops(bezier_curves):
    """
    Identifies loops in a list of Bezier curves.

    Parameters:
    bezier_curves: list of tuples
        List of Bezier curves represented by their control points.

    Returns:
    list of lists
        List of loops, where each loop is a list of Bezier curves.
    """
    curves_to_plot = []
    used = set()
    
    def find_next_curve(start_point):
        for idx, curve in enumerate(bezier_curves):
            if idx not in used and points_match(curve[0], start_point):
                used.add(idx)
                return idx
        return None

    for idx, curve in enumerate(bezier_curves):
        if idx not in used:
            start_point = curve[0]
            used.add(idx)
            loop = [curve]
            while True:
                next_idx = find_next_curve(curve[3])
                if next_idx is None:
                    break
                loop.append(bezier_curves[next_idx])
                curve = bezier_curves[next_idx]
            
            if points_match(loop[-1][3], loop[0][0]):
                curves_to_plot.append(loop)
    
    return curves_to_plot

def fit_circle(points):
    """
    Fits a circle to a set of points.

    Parameters:
    points: np.array
        Array of points to fit the circle to.

    Returns:
    tuple
        Parameters of the fitted circle (x_center, y_center, radius).
    """
    def objective(params):
        x0, y0, r = params
        distances = np.sqrt((points[:,0] - x0)**2 + (points[:,1] - y0)**2)
        return distances - r

    x_mean, y_mean = np.mean(points, axis=0)
    r_guess = np.mean(np.sqrt((points[:,0] - x_mean)**2 + (points[:,1] - y_mean)**2))
    initial_guess = [x_mean, y_mean, r_guess]

    result, _ = leastsq(objective, initial_guess)
    return result

def check_circularity_and_fit(loop, radius_threshold=5):
    """
    Checks if a loop of Bezier curves forms a circle and fits the circle.

    Parameters:
    loop: list of tuples
        List of Bezier curves representing the loop.
    radius_threshold: float
        Threshold for the maximum distance deviation to consider as a circle.

    Returns:
    tuple or None
        Parameters of the fitted circle (x_center, y_center, radius) if circular, otherwise None.
    """
    all_points = []
    for curve in loop:
        p0, p1, p2, p3 = curve
        t_values = np.linspace(0, 1, 100)
        curve_points = np.array([bezier_curve_cubic(p0, p1, p2, p3, t) for t in t_values])
        all_points.extend(curve_points)
    
    all_points = np.array(all_points)
    
    circle_params = fit_circle(all_points)
    x_center, y_center, radius = circle_params
    
    distances = np.sqrt((all_points[:,0] - x_center)**2 + (all_points[:,1] - y_center)**2)
    max_distance = np.max(distances)
    
    if abs(max_distance - radius) <= radius_threshold:
        return (x_center, y_center, radius)
    return None

def process_bezier_and_circles(bezier_curves):
    """
    Processes a list of Bezier curves to find loops and fit circles to them.

    Parameters:
    bezier_curves: list of tuples
        List of Bezier curves represented by their control points.

    Returns:
    tuple
        Non-looped curves, looped curves, and circle fits.
    """
    def curve_to_tuple(curve):
        return tuple(map(tuple, curve))
    
    def tuple_to_curve(tpl):
        return np.array(tpl)
    
    bezier_curves_tuples = [curve_to_tuple(curve) for curve in bezier_curves]
    
    loops = find_loops(bezier_curves)
    print(f"Number of loops detected: {len(loops)}")
    
    used_curves = set()
    
    circle_fits = []
    non_looped_curves = []
    looped = []
    
    for loop in loops:
        fit_result = check_circularity_and_fit(loop)
        if fit_result:
            x_center, y_center, radius = fit_result
            circle_fits.append((x_center, y_center, radius))
        else:
            looped.extend(loop)
        used_curves.update(curve_to_tuple(curve) for curve in loop)
    
    non_looped_curves = [curve for curve in bezier_curves if curve_to_tuple(curve) not in used_curves]
    
    loops = [list(map(tuple_to_curve, loop)) for loop in loops]
    looped = [tuple_to_curve(curve) for curve in looped]
    
    return non_looped_curves, looped, circle_fits
