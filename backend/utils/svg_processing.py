import csv
from collections import defaultdict
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

class SVGProcessor:
    def __init__(self, csv_data: str):
        self.csv_data = csv_data
        self.all_points = []

    def extract_points_from_csv(self):
        csv_reader = csv.reader(self.csv_data.splitlines())
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            curve_index, static, x, y = int(row[0]), float(row[1]), float(row[2]), float(row[3])
            self.all_points.append((curve_index, static, x, y))
