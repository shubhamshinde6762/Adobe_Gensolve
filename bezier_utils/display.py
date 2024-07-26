import matplotlib.pyplot as plt
import numpy as np
from .attributes import osculating_circle_center
from .core import bezier_curve
from .linearity import is_approximately_linear_by_curvature, is_approximately_linear

def plot_bezier_curves_by_cross_linear(cubic_points, quadratic_points, threshold=1.0, linear_tolerance=0.1, show_control=False, show_centers=True):
    """
    Plot cubic and quadratic Bézier curves, highlighting curves that are approximately linear.

    Args:
        cubic_points (numpy.ndarray): Array of control points for cubic Bézier curves. 
                                      Each cubic Bézier curve is represented by a set of four control points.
        quadratic_points (numpy.ndarray): Array of control points for quadratic Bézier curves.
                                          Each quadratic Bézier curve is represented by a set of three control points.
        threshold (float): Distance threshold for filtering osculating circle centers. 
                            Osculating circle centers within this distance from the curve will be plotted.
        linear_tolerance (float): Maximum allowable deviation from linearity to consider a Bézier curve as approximately linear.

    Notes:
        - The function generates a plot for both cubic and quadratic Bézier curves.
        - Control points and osculating circle centers are currently commented out, but they can be included by uncommenting the relevant lines.
        - The function checks if the Bézier curves are approximately linear and plots a dashed line between the start and end points if they are.
    """
    plt.figure(figsize=(10, 10))
    
    # Plot cubic Bézier curves
    for points in cubic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Cubic Bezier', color=color)
        if(show_control):
            plt.plot(points[:, 0], points[:, 1], 'ro--')  
        if(show_centers):
            plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Uncomment to plot osculating circle centers
        
        if is_approximately_linear(curve, linear_tolerance):
            plt.plot([points[0][0], points[-1][0]], [points[0][1], points[-1][1]], 'k--', label='Approx. Linear')

    # Plot quadratic Bézier curves
    for points in quadratic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Quadratic Bezier', color=color)
        if(show_control):
            plt.plot(points[:, 0], points[:, 1], 'bo--')  # Uncomment to plot control points
        if(show_centers):
            plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Uncomment to plot osculating circle centers
        
        if is_approximately_linear(curve, linear_tolerance):
            plt.plot([points[0][0], points[-1][0]], [points[0][1], points[-1][1]], 'k--', label='Approx. Linear')
    
    # Display plot
    plt.title('Bezier Curves with Approximate Linearity')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.show()




def plot_bezier_curves_by_curvature(cubic_points, quadratic_points, threshold=1.0, curvature_tolerance=0.01, show_control=False, show_centers=True):
    """
    Plot Bézier curves, their control points, osculating circle centers, and approximate linear segments based on curvature.

    Args:
        cubic_points (numpy.ndarray): Control points for cubic Bézier curves.
        quadratic_points (numpy.ndarray): Control points for quadratic Bézier curves.
        threshold (float): Distance threshold for osculating circle centers.
        curvature_tolerance (float): Tolerance for determining if a curve is approximately linear based on curvature.
    """
    plt.figure(figsize=(10, 10))
    
    for points in cubic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Cubic Bezier', color=color)
        if(show_control):       
            plt.plot(points[:, 0], points[:, 1], 'ro--')  # Control points
        if(show_centers):
            plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Osculating circle centers
        
        if is_approximately_linear_by_curvature(curve, curvature_tolerance):
            plt.plot([points[0][0], points[-1][0]], [points[0][1], points[-1][1]], 'k--', label='Approx. Linear')

    for points in quadratic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Quadratic Bezier', color=color)
        if(show_control):  
            plt.plot(points[:, 0], points[:, 1], 'bo--')  # Control points
        if(show_centers):  
            plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Osculating circle centers
        
        if is_approximately_linear_by_curvature(curve, curvature_tolerance):
            plt.plot([points[0][0], points[-1][0]], [points[0][1], points[-1][1]], 'k--', label='Approx. Linear')
    
    #plt.legend()
    plt.title('Bezier Curves with Osculating Circle Centers')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.show()




def plot_bezier_curves(cubic_points, quadratic_points, threshold=1.0):
    plt.figure(figsize=(10, 10))
    
    for points in cubic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Cubic Bezier', color=color)
        #plt.plot(points[:, 0], points[:, 1], 'ro--')  # Control points
        plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Osculating circle centers
    
    for points in quadratic_points:
        curve = bezier_curve(points)
        centers = osculating_circle_center(points, threshold)
        color = np.random.rand(3,)  # Random color for each curve
        plt.plot(curve[:, 0], curve[:, 1], label='Quadratic Bezier', color=color)
        plt.plot(points[:, 0], points[:, 1], 'bo--')  # Control points
        plt.plot(centers[:, 0], centers[:, 1], 'x', label='Osculating Circle Centers', color=color)  # Osculating circle centers
    
    #plt.legend()
    plt.title('Bezier Curves with Osculating Circle Centers')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.show()