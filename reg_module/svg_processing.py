from svgpathtools import svg2paths, Path, Line, CubicBezier, QuadraticBezier, Arc
import numpy as np
import csv
from collections import defaultdict
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

class SVGProcessor:
    def __init__(self, svg_file: str):
        self.svg_file = svg_file
        self.all_points = []

    def extract_points_from_path(self, path_segment, num_samples=100):
        if isinstance(path_segment, (Line, CubicBezier, QuadraticBezier, Arc)):
            return [path_segment.point(t) for t in np.linspace(0, 1, num_samples)]
        return []

    def extract_all_points(self):
        paths, _ = svg2paths(self.svg_file)
        for curve_index, path in enumerate(paths):
            for segment in path:
                points = self.extract_points_from_path(segment)
                self.all_points.extend([(curve_index, 0.0000, float(p.real), float(p.imag)) for p in points])



# Example usage
