import matplotlib.pyplot as plt
import numpy as np

def plot_polygon(lines):
    """
    Plots a series of line segments on a 2D graph.

    This function takes a list of line segments, where each line segment is represented
    as a 2x2 numpy array with coordinates of two endpoints. It plots these line segments
    on a 2D graph using matplotlib, with markers indicating the endpoints.

    Parameters:
    - lines (list of np.ndarray): A list of line segments, where each line segment is 
      represented as a 2x2 numpy array. Each array contains two points, with each point
      specified by its x and y coordinates.

    Returns:
    - None: This function does not return any value. It displays the plot directly.
    """
    plt.figure()
    for line in lines:
        x_values = line[:, 0]
        y_values = line[:, 1]
        plt.plot(x_values, y_values, marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Plot of Given Line Segments')
    plt.show()




def plot_arrows_between_points(points):
    """
    Plots arrows connecting sequential points on a 2D graph.

    This function takes a list of points, represented as tuples or lists of coordinates, and
    plots arrows between each consecutive pair of points to visualize the sequence.

    Parameters:
    - points (list of tuple or list): A list of points where each point is represented as a
      tuple or list with coordinates (x, y). The points should be in the order they should
      be connected.

    Returns:
    - None: This function does not return any value. It displays the plot directly.
    """
    # Convert points to numpy array for easy manipulation
    points = np.array(points)

    plt.figure()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Arrows Connecting Sequential Points')

    # Plot arrows between consecutive points
    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]
        plt.arrow(start_point[0], start_point[1],
                  end_point[0] - start_point[0], end_point[1] - start_point[1],
                  head_width=5, head_length=10, fc='blue', ec='blue')

    # Optionally plot the last point connected to the first point to form a loop
    if len(points) > 1:
        plt.arrow(points[-1][0], points[-1][1],
                  points[0][0] - points[-1][0], points[0][1] - points[-1][1],
                  head_width=5, head_length=5, fc='blue', ec='blue')

    plt.scatter(points[:, 0], points[:, 1], color='red')  # Plot the points themselves
    plt.grid(True)
    plt.show()