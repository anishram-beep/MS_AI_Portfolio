#import pandas as pd
#import numpy as np
#from sklearn.cluster import KMeans
#from sklearn.cluster import SpectralClustering

from Truck import Truck
from Package import Package
from datetime import datetime


#010538440
class DeliveryManager:

    """
    A class to manage delivery operations including the creation of an adjacency matrix.
    """
    # distance_matrix_np = 0
    # Dictionary linking package IDs with address and corresponding matrix row index

    package_dictionary ={
        1: {"Address": "195 W Oakland Ave", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
            "Delivery Deadline": "10:30 AM", "Weight-KILO": 21},
        2: {"Address": "2530 S 500 E", "City": "Salt Lake City", "State": "UT", "Zip": "84106",
            "Delivery Deadline": "EOD", "Weight-KILO": 44},
        3: {"Address": "233 Canyon Rd", "City": "Salt Lake City", "State": "UT", "Zip": "84103",
            "Delivery Deadline": "EOD", "Weight-KILO": 2},
        4: {"Address": "380 W 2880 S", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
            "Delivery Deadline": "EOD", "Weight-KILO": 4},
        5: {"Address": "410 S State St", "City": "Salt Lake City", "State": "UT", "Zip": "84111",
            "Delivery Deadline": "EOD", "Weight-KILO": 5},
        6: {"Address": "3060 Lester St", "City": "West Valley City", "State": "UT", "Zip": "84119",
            "Delivery Deadline": "10:30 AM", "Weight-KILO": 88},
        7: {"Address": "1330 2100 S", "City": "Salt Lake City", "State": "UT", "Zip": "84106",
            "Delivery Deadline": "EOD", "Weight-KILO": 8},
        8: {"Address": "300 State St", "City": "Salt Lake City", "State": "UT", "Zip": "84103",
            "Delivery Deadline": "EOD", "Weight-KILO": 9},
        9: {"Address": "300 State St", "City": "Salt Lake City", "State": "UT", "Zip": "84103",
            "Delivery Deadline": "EOD", "Weight-KILO": 2},
        10: {"Address": "600 E 900 South", "City": "Salt Lake City", "State": "UT", "Zip": "84105",
             "Delivery Deadline": "EOD", "Weight-KILO": 1},
        11: {"Address": "2600 Taylorsville Blvd", "City": "Salt Lake City", "State": "UT", "Zip": "84118",
             "Delivery Deadline": "EOD", "Weight-KILO": 1},
        12: {"Address": "3575 W Valley Central Station bus Loop", "City": "West Valley City", "State": "UT",
             "Zip": "84119", "Delivery Deadline": "EOD", "Weight-KILO": 1},
        13: {"Address": "2010 W 500 S", "City": "Salt Lake City", "State": "UT", "Zip": "84104",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 2},
        14: {"Address": "4300 S 1300 E", "City": "Millcreek", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 88},
        15: {"Address": "4580 S 2300 E", "City": "Holladay", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "9:00 AM", "Weight-KILO": 4},
        16: {"Address": "4580 S 2300 E", "City": "Holladay", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 88},
        17: {"Address": "3148 S 1100 W", "City": "Salt Lake City", "State": "UT", "Zip": "84119",
             "Delivery Deadline": "EOD", "Weight-KILO": 2},
        18: {"Address": "1488 4800 S", "City": "Salt Lake City", "State": "UT", "Zip": "84123",
             "Delivery Deadline": "EOD", "Weight-KILO": 6},
        19: {"Address": "177 W Price Ave", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
             "Delivery Deadline": "EOD", "Weight-KILO": 37},
        20: {"Address": "3595 Main St", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 37},
        21: {"Address": "3595 Main St", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
             "Delivery Deadline": "EOD", "Weight-KILO": 3},
        22: {"Address": "6351 South 900 East", "City": "Murray", "State": "UT", "Zip": "84121",
             "Delivery Deadline": "EOD", "Weight-KILO": 2},
        23: {"Address": "5100 South 2700 West", "City": "Salt Lake City", "State": "UT", "Zip": "84118",
             "Delivery Deadline": "EOD", "Weight-KILO": 5},
        24: {"Address": "5025 State St", "City": "Murray", "State": "UT", "Zip": "84107", "Delivery Deadline": "EOD",
             "Weight-KILO": 7},
        25: {"Address": "5383 South 900 East #104", "City": "Salt Lake City", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 7},
        26: {"Address": "5383 South 900 East #104", "City": "Salt Lake City", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "EOD", "Weight-KILO": 25},
        27: {"Address": "1060 Dalton Ave S", "City": "Salt Lake City", "State": "UT", "Zip": "84104",
             "Delivery Deadline": "EOD", "Weight-KILO": 5},
        28: {"Address": "2835 Main St", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
             "Delivery Deadline": "EOD", "Weight-KILO": 7},
        29: {"Address": "1330 2100 S", "City": "Salt Lake City", "State": "UT", "Zip": "84106",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 2},
        30: {"Address": "300 State St", "City": "Salt Lake City", "State": "UT", "Zip": "84103",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 1},
        31: {"Address": "3365 S 900 W", "City": "Salt Lake City", "State": "UT", "Zip": "84119",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 1},
        32: {"Address": "3365 S 900 W", "City": "Salt Lake City", "State": "UT", "Zip": "84119",
             "Delivery Deadline": "EOD", "Weight-KILO": 1},
        33: {"Address": "2530 S 500 E", "City": "Salt Lake City", "State": "UT", "Zip": "84106",
             "Delivery Deadline": "EOD", "Weight-KILO": 1},
        34: {"Address": "4580 S 2300 E", "City": "Holladay", "State": "UT", "Zip": "84117",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 2},
        35: {"Address": "1060 Dalton Ave S", "City": "Salt Lake City", "State": "UT", "Zip": "84104",
             "Delivery Deadline": "EOD", "Weight-KILO": 88},
        36: {"Address": "2300 Parkway Blvd", "City": "West Valley City", "State": "UT", "Zip": "84119",
             "Delivery Deadline": "EOD", "Weight-KILO": 88},
        37: {"Address": "410 S State St", "City": "Salt Lake City", "State": "UT", "Zip": "84111",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 2},
        38: {"Address": "410 S State St", "City": "Salt Lake City", "State": "UT", "Zip": "84111",
             "Delivery Deadline": "EOD", "Weight-KILO": 9},
        39: {"Address": "2010 W 500 S", "City": "Salt Lake City", "State": "UT", "Zip": "84104",
             "Delivery Deadline": "EOD", "Weight-KILO": 9},
        40: {"Address": "380 W 2880 S", "City": "Salt Lake City", "State": "UT", "Zip": "84115",
             "Delivery Deadline": "10:30 AM", "Weight-KILO": 45}

    }
    package_list = {
        1: {"address": "195 W Oakland Ave", "matrix_index": 4},
        2: {"address": "2530 S 500 E", "matrix_index": 8},
        3: {"address": "233 Canyon Rd", "matrix_index": 7},
        4: {"address": "380 W 2880 S", "matrix_index": 17},
        5: {"address": "410 S State St", "matrix_index": 18},
        6: {"address": "3060 Lester St", "matrix_index": 12},
        7: {"address": "1330 2100 S", "matrix_index": 1},
        8: {"address": "300 State St", "matrix_index": 11},
        9: {"address": "300 State St", "matrix_index": 11},
        10: {"address": "600 E 900 South", "matrix_index": 24},
        11: {"address": "2600 Taylorsville Blvd", "matrix_index": 9},
        12: {"address": "3575 W Valley Central Station bus Loop", "matrix_index": 15},
        13: {"address": "2010 W 500 S", "matrix_index": 5},
        14: {"address": "4300 S 1300 E", "matrix_index": 19},
        15: {"address": "4580 S 2300 E", "matrix_index": 20},
        16: {"address": "4580 S 2300 E", "matrix_index": 20},
        17: {"address": "3148 S 1100 W", "matrix_index": 13},
        18: {"address": "1488 4800 S", "matrix_index": 2},
        19: {"address": "177 W Price Ave", "matrix_index": 3},
        20: {"address": "3595 Main St", "matrix_index": 16},
        21: {"address": "3595 Main St", "matrix_index": 16},
        22: {"address": "6351 South 900 East", "matrix_index": 25},
        23: {"address": "5100 South 2700 West", "matrix_index": 22},
        24: {"address": "5025 State St", "matrix_index": 21},
        25: {"address": "5383 S 900 East #104", "matrix_index": 23},
        26: {"address": "5383 S 900 East #104", "matrix_index": 23},
        27: {"address": "1060 Dalton Ave S", "matrix_index": 0},
        28: {"address": "2835 Main St", "matrix_index": 10},
        29: {"address": "1330 2100 S", "matrix_index": 1},
        30: {"address": "300 State St", "matrix_index": 11},
        31: {"address": "3365 S 900 W", "matrix_index": 14},
        32: {"address": "3365 S 900 W", "matrix_index": 14},
        33: {"address": "2530 S 500 E", "matrix_index": 8},
        34: {"address": "4580 S 2300 E", "matrix_index": 20},
        35: {"address": "1060 Dalton Ave S", "matrix_index": 0},
        36: {"address": "2300 Parkway Blvd", "matrix_index": 6},
        37: {"address": "410 S State St", "matrix_index": 18},
        38: {"address": "410 S State St", "matrix_index": 18},
        39: {"address": "2010 W 500 S", "matrix_index": 5},
        40: {"address": "380 W 2880 S", "matrix_index": 17}
    }

    package_info = {
        1: {"count": 1, "duplicates": []},
        2: {"count": 1, "duplicates": []},
        3: {"count": 1, "duplicates": []},
        4: {"count": 2, "duplicates": [40]},  # Package ID 4 has the same location as 40
        5: {"count": 3, "duplicates": [37, 38]},  # Package ID 5 shares location with 37 and 38
        6: {"count": 1, "duplicates": []},
        7: {"count": 1, "duplicates": []},
        8: {"count": 3, "duplicates": [9, 30]},  # Package ID 8 shares location with 9 and 30
        9: {"count": 3, "duplicates": [8, 30]},  # Same as above
        10: {"count": 1, "duplicates": []},
        11: {"count": 1, "duplicates": []},
        12: {"count": 1, "duplicates": []},
        13: {"count": 1, "duplicates": []},
        14: {"count": 1, "duplicates": []},
        15: {"count": 2, "duplicates": [16]},  # Package ID 15 shares location with 16
        16: {"count": 2, "duplicates": [15]},  # Same as above
        17: {"count": 1, "duplicates": []},
        18: {"count": 1, "duplicates": []},
        19: {"count": 1, "duplicates": []},
        20: {"count": 2, "duplicates": [21]},  # Package ID 20 shares location with 21
        21: {"count": 2, "duplicates": [20]},  # Same as above
        22: {"count": 1, "duplicates": []},
        23: {"count": 1, "duplicates": []},
        24: {"count": 1, "duplicates": []},
        25: {"count": 2, "duplicates": [26]},  # Package ID 25 shares location with 26
        26: {"count": 2, "duplicates": [25]},  # Same as above
        27: {"count": 2, "duplicates": [35]},  # Package ID 27 shares location with 35
        28: {"count": 1, "duplicates": []},
        29: {"count": 1, "duplicates": []},
        30: {"count": 3, "duplicates": [8, 9]},  # Same as above for Package ID 8
        31: {"count": 2, "duplicates": [32]},  # Package ID 31 shares location with 32
        32: {"count": 2, "duplicates": [31]},  # Same as above
        33: {"count": 1, "duplicates": []},
        34: {"count": 1, "duplicates": []},
        35: {"count": 2, "duplicates": [27]},  # Same as above for Package ID 27
        36: {"count": 1, "duplicates": []},
        37: {"count": 3, "duplicates": [5, 38]},  # Same as above for Package ID 5
        38: {"count": 3, "duplicates": [5, 37]},  # Same as above for Package ID 5
        39: {"count": 1, "duplicates": []},
        40: {"count": 2, "duplicates": [4]},  # Same as above for Package ID 4
    }

    def __init__(self):
        # Initialize any variables if needed in the future
        self.distance_matrix_np = self.create_distance_matrix()
        self.labels = None
        Package(package_id = 0, location = 0)
        for package_id in range(1, 41):  # Assuming package IDs from 1 to 40
            Package(package_id, location=self.package_dictionary[package_id]["State"], delivery_address= self.package_dictionary[package_id]["Address"], delivery_deadline=self.package_dictionary[package_id]["Delivery Deadline"],
                 delivery_city=self.package_dictionary[package_id]["City"], delivery_zipcode=self.package_dictionary[package_id]["Zip"], package_weight=self.package_dictionary[package_id]["Weight-KILO"])  # Location 0 as a placeholder


   # def run_initial_cluster(self):
    #    n = 2

        # Initialize and fit KMeans
       # kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)

        # Fit K-means on the adjacency matrix (distances between locations)
        #labels = kmeans.fit_predict(self.distance_matrix_np)
        # Apply Spectral Clustering with the adjacency matrix

     #   spectral = SpectralClustering(n, affinity='precomputed', random_state=42)
     #   self.labels = spectral.fit_predict(self.distance_matrix_np)

        # Output the clusters
    #    print("Cluster assignments using Spectral Clustering:")
     #   print(self.labels + 1)
        # Output the cluster assignments for each package


    def create_distance_matrix(self):
        """
        Creates the distance matrix as a NumPy array and prints it.
        """

        # Manually enter the matrix data as a 2D list
        distance_matrix = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [7.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.8, 7.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [11.0, 6.4, 9.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [2.2, 6.0, 4.4, 5.6, 0.0 , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.5, 4.8, 2.8, 6.9, 1.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [10.9, 1.6, 8.6, 8.6, 7.9, 6.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [8.6, 2.8, 6.3, 4.0, 5.1, 4.3, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [2.8, 6.3, 1.6, 7.3, 2.6, 1.5, 8.0, 9.3, 4.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [6.4, 7.3, 10.4, 1.0, 6.5, 8.7, 8.6, 4.6, 11.9, 9.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.2, 5.3, 3.0, 6.4, 1.5, 0.8, 6.9, 4.8, 4.7, 1.1, 7.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0.6, 5.1, 12.0, 4.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [5.2, 3.0, 6.5, 3.9, 3.2, 3.9, 4.2, 1.6, 7.6, 4.6, 4.9, 3.5, 7.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [4.4, 4.6, 5.6, 4.3, 2.4, 3.0, 8.0, 3.3, 7.8, 3.7, 5.2, 2.6, 7.8, 1.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.7, 4.5, 5.8, 4.4, 2.7, 3.8, 5.8, 3.4, 6.6, 4.0, 5.4, 2.9, 6.6, 1.5, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [7.6, 7.4, 5.7, 7.2, 1.4, 5.7, 7.2, 3.1, 7.2, 6.7, 8.1, 6.3, 7.2, 4.0, 6.4, 5.6, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [2.0, 6.0, 4.1, 5.3, 0.5, 1.9, 7.7, 5.1, 5.9, 2.3, 6.2, 1.2, 5.9, 3.2, 2.4, 1.6, 7.1, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.6, 5.0, 3.6, 6.0, 1.7, 1.1, 6.6, 4.6, 5.4, 1.8, 6.9, 1.0, 5.4, 3.0, 2.2, 1.7, 6.1, 1.6, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [6.5, 4.8, 4.3, 10.6, 6.5, 3.5, 3.2, 6.7, 1.0, 4.1, 11.5, 3.7, 1.0, 6.9, 6.8, 6.4, 7.2, 4.9, 4.4, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.9, 9.5, 3.3, 5.9, 3.2, 4.9, 11.2, 8.1, 8.5, 3.8, 6.9, 4.1, 8.5, 6.2, 5.3, 4.9, 10.6, 3.0, 4.6, 7.5,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.4, 10.9, 5.0, 7.4, 5.2, 6.9, 12.7, 10.4, 10.3, 5.8, 8.3, 6.2, 10.3, 8.2, 7.4, 6.9, 12.0, 5.0, 6.6,
             9.3, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [2.4, 8.3, 6.1, 4.7, 2.5, 4.2, 10.0, 7.8, 7.8, 4.3, 4.1, 3.4, 7.8, 5.5, 4.6, 4.2, 9.4, 2.3, 3.9, 6.8,
             2.9, 4.4, 0.0, 0.0, 0.0, 0.0, 0.0],
            [6.4, 6.9, 9.7,   0.6, 6.0, 9.0, 8.2, 4.2, 11.5, 7.8, 0.4, 6.9, 11.5, 4.4, 4.8, 5.6, 7.5, 5.5, 6.5, 11.4,
             6.4, 7.9, 4.5, 0.0, 0.0, 0.0, 0.0],
            [2.4, 10.0, 6.1, 6.4, 4.2, 5.9, 11.7, 9.5, 9.5, 4.8, 4.9, 5.2, 9.5, 7.2, 6.3, 5.9, 11.1, 4.0, 5.6, 8.5,
             2.8, 3.4, 1.7, 5.4, 0.0, 0.0, 0.0],
            [5.0, 4.4, 2.8, 10.1, 5.4, 3.5, 5.1, 6.2, 2.8, 3.2, 11.0, 3.7, 2.8, 6.4, 6.5, 5.7, 6.2, 5.1, 4.3, 1.8,
             6.0, 7.9, 6.8, 10.6, 7.0, 0.0, 0.0],
            [3.6, 13.0, 7.4, 10.1, 5.5, 7.2, 14.2, 10.7, 14.1, 6.0, 6.8, 6.4, 14.1, 10.5, 8.8, 8.4, 13.6, 5.2, 6.9,
             13.1, 4.1, 4.7, 3.1, 7.8, 1.3, 8.3, 0.0]
        ]

        # Convert the list to a NumPy array
      #  self.distance_matrix_np = np.array(distance_matrix)

        self.distance_matrix_np = distance_matrix


        # Print the matrix for verification
        print("Adjacency Matrix:")
        print(self.distance_matrix_np)

        return self.distance_matrix_np
    def main(self):
        """
        Entry point for the DeliveryManager to run its operations.
        """
       # self.create_distance_matrix()
      #  from Truck import Truck

        optimal_route = None
        min_distance = None
        d_list = None
        package_tList = []

        dmanager = DeliveryManager()
        print(" ")
     #   dmanager.run_initial_cluster()
     #   self.labels = np.array([2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2])

        self.truck1 = Truck(truck_id=1, package_list=self.package_list,  distance_matrix_np=self.distance_matrix_np)
        self.truck1.assign_packages2()

        self.truck2 = Truck(truck_id=2,  package_list=self.package_list, distance_matrix_np=self.distance_matrix_np)
        self.truck2.assign_packages2()

        self.truck3 = Truck(truck_id=3,  package_list=self.package_list, distance_matrix_np=self.distance_matrix_np)
        self.truck3.assign_packages2()


       # print(self.truck1.current_packages)
       # print(self.truck2.current_packages)
       # print(self.truck3.current_packages)



        total_distance = 0
        list_package_delivery = []

        print(" ")
        print("All Packages except (6,25,28,32) at Depot at 8:00 AM")
        print("All Packages (6,25,28,32) at Depot at 9:20 AM")
        self.truck1.current_packages = [pkg for pkg in self.truck1.current_packages if pkg not in (25, 6)] + [pkg for pkg in self.truck1.current_packages if pkg in (25, 6)]
        print("Truck 1 loaded with packages at 8:00 AM:")
        print(self.truck1.current_packages)

        print(" ")


        print("Truck 1 Path (package_id, location) {distance values and intermediate distance between the split route shown below}:")
        self.truck1.perform_brute_force_for_truck(self.truck1.current_packages)
        # Initialize counters and time variables
        counter = 0
        rate_of_truck = 18  # Speed of truck in miles per hour
        time = 8.0  # Start time at 8:00 AM

        # Calculate total route and update each package in Truck 1's route
        all_routes = self.truck1.optimal_routep1 + self.truck1.optimal_routep2
        intermediate_distance = [self.distance_matrix_np[self.truck1.optimal_routep2[0][1]][self.truck1.optimal_routep1[len(self.truck1.optimal_routep1)-1][1]]]
        print(intermediate_distance)
        all_distances = self.truck1.d_listp1 + intermediate_distance + self.truck1.d_listp2

       # truck1_departure_time = datetime.strptime("08:00:00 AM", "%I:%M:%S %p")

        for x in all_routes:

            if x[1] == 0:
             package = Package.get_package(x[1])
            else:
             package = Package.get_package(x[0])
             package.status = "En Route"

            if package.package_id != 0:
                print(package.info())
                list_package_delivery.append(package.info())
           # else:
           #     print(f"Package with ID {x[1]} not found.")



        counter = 0
        for idx, (package_id, location) in enumerate(all_routes):
            if location == 0:
             package = Package.get_package(0)
            else:
             package = Package.get_package(package_id)

            if package:
                # Calculate delivery time for each package
                if counter > 0:
                 distance_travelled = sum(all_distances[:idx])

                else:
                    distance_travelled = 0

                time = 8 + (distance_travelled / rate_of_truck)

                # Update the delivery status and time
                if package.package_id != 0:
                    package.status = "delivered"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM"  # Format time for each package as it's delivered
                    print(package.info())
                    list_package_delivery.append(package.info())

                    package_tList.append("Truck 1:" + package.info())
                else:
                    package.status = "At Hub"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM"   # Format time for each package as it's delivered
                    print(package.info())

                    package_tList.append("Truck 1:" + package.info())

            if idx == len(all_routes) - 1:

                total_distance  = total_distance + distance_travelled


            counter = counter + 1

 #       for x in all_routes:
 #           if x[1] == 0:
            # package = Package.get_package(location)
 #            package = Package.get_package(x[1])
  #          else:
 #            package = Package.get_package(x[0])
#
 #           print(package.info())


       # distance_travelled = sum(all_distances[:len(all_distances)]) if counter > 0 else distance_travelled == sum(all_distances[0])
       # time = 8 + (distance_travelled / rate_of_truck)

        print(" ")
        print("Truck 1 finished delivery at: ")
        truck1_startTime = 8.0
        truck1_endTime = time
        print(f"{int(time)}:{int((time % 1) * 60):02d} AM")
        print(" ")

        print("Truck 2 loaded with packages at 8:00 AM:")
        print(self.truck2.current_packages)

        print("Truck 2 Path (package_id, location) {distance values and intermediate distance between the split route shown below}:")
        self.truck2.perform_brute_force_for_truck(self.truck2.current_packages)
        # Initialize counters and time variables
        counter = 0
        rate_of_truck = 18  # Speed of truck in miles per hour
        time = 8.0  # Start time at 8:00 AM

        # Calculate total route and update each package in Truck 2's route
        all_routes = self.truck2.optimal_routep1 + self.truck2.optimal_routep2
        intermediate_distance = [self.distance_matrix_np[self.truck2.optimal_routep1[len(self.truck2.optimal_routep1) - 1][1]][self.truck2.optimal_routep2[0][1]]]
        print(intermediate_distance)
        all_distances = self.truck2.d_listp1 + intermediate_distance + self.truck2.d_listp2

        for x in all_routes:

            if x[1] == 0:
                package = Package.get_package(x[1])
            else:
                package = Package.get_package(x[0])
                package.status = "En Route"

            if package.package_id != 0:
                print(package.info())
        # else:
        #     print(f"Package with ID {x[1]} not found.")

        counter = 0
        for idx, (package_id, location) in enumerate(all_routes):
            if location == 0:
                package = Package.get_package(0)
            else:
                package = Package.get_package(package_id)

            if package:
                # Calculate delivery time for each package
                if counter > 0:
                    distance_travelled = sum(all_distances[:idx])

                else:
                    distance_travelled = 0

                time = 8 + (distance_travelled / rate_of_truck)

                # Update the delivery status and time
                if package.package_id != 0:
                    package.status = "delivered"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM"  # Format time for each package as it's delivered
                    print(package.info())
                    list_package_delivery.append(package.info())
                    package_tList.append("Truck 2:" + package.info())

                else:
                    package.status = "At Hub"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM"  # Format time for each package as it's delivered
                    print(package.info())
                    package_tList.append("Truck 2:" + package.info())


            if idx == len(all_routes) - 1:
                total_distance = total_distance + distance_travelled

            counter = counter + 1
        #  self.truck2.optimal_routep1
      #  self.truck2.min_distancep1
      #  self.truck2.d_listp1

      #  self.truck2.optimal_routep2
      #  self.truck2.min_distancep2
      #  self.truck2.d_listp2

        print(" ")
        print("Truck 2 finished delivery at: ")
        truck2_startTime = 8.0
        truck2_endTime = time
        print(f"{int(time)}:{int((time % 1) * 60):02d} AM")
        print(" ")

        truck3_startTime = time

        print("Truck 3 loaded with packages at ")
        print(f"{int(time)}:{int((time % 1) * 60):02d} AM")
        print(self.truck3.current_packages)
        print("Package 9 address updated 10:20 am")

        print("Truck 3 Path (package_id, location) {distance values and intermediate distance between the split route shown below}:")
        self.truck3.perform_brute_force_for_truck(self.truck3.current_packages)
        # Initialize counters and time variables
        counter = 0
        rate_of_truck = 18  # Speed of truck in miles per hour
        time = 9+ 56/60  # Start time based on truck 2

        # Calculate total route and update each package in Truck 3's route
        all_routes = self.truck3.optimal_routep1
        intermediate_distance = 0
        print(intermediate_distance)
        all_distances = self.truck3.d_listp1


        for x in all_routes:

            if x[1] == 0:
                package = Package.get_package(x[1])
            else:
                package = Package.get_package(x[0])
                package.status = "En Route"

            if package.package_id != 0:
                print(package.info())
        # else:
        #     print(f"Package with ID {x[1]} not found.")

        counter = 0
        for idx, (package_id, location) in enumerate(all_routes):

            if location == 0:
                package = Package.get_package(0)
            else:
                package = Package.get_package(package_id)

            if package_id == 9:
                package.delivery_address = "410 S. State St."
                package.location = "UT",
                package.delivery_city = "Salt Lake City"
                package.delivery_zipcode = "84111"  # Location 0 as a placeholder

            if package:
                # Calculate delivery time for each package
                if counter > 0:
                    distance_travelled = sum(all_distances[:idx])

                else:
                    distance_travelled = 0

                time = 9+ 56/60  + (distance_travelled / rate_of_truck)

                # Update the delivery status and time
                if package.package_id != 0:
                    package.status = "delivered"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM" # Format time for each package as it's delivered
                    print(package.info())
                    list_package_delivery.append(package.info())

                    package_tList.append("Truck 3:" + package.info())

                else:
                    package.status = "At Hub"
                    package.delivery_time = f"{int(time)}:{int((time % 1) * 60):02d}:{int(((time * 60) % 1) * 60):02d} AM" # Format time for each package as it's delivered
                    print(package.info())
                    package_tList.append("Truck 3:" + package.info())


            if idx == len(all_routes) - 1:
                total_distance = total_distance + distance_travelled

            counter = counter + 1

        truck3_endTime = time
        print("Truck 3 finished delivery at ")
        print(f"{int(time)}:{int((time % 1) * 60):02d} AM")
      #  print("7.2 miles back to hub")
        print("Total Distance Travelled")
        print(total_distance)
        store = 1









        # Filter and sort based on delivery time
        sorted_package_times = sorted(
            (item for item in package_tList if "Delivery Time:" in item),
            key=lambda x: datetime.strptime(
                x.split("Delivery Time: ")[1].split(",")[0].strip(), "%I:%M:%S %p"
            )
        )

        # Print sorted packages
     #   for package in sorted_package_times:
     #       if "(0" not in package:
      #       print(package)

        # while store != "-1":
        #      print("Enter package id and enter (-1) to go to the next menu option")
        #      store = input()
        #
        #      for val in sorted_package_times:
        #         if f"Package({store}," in val:
        #            print(val)

        end_time_str = 0
        while end_time_str != -1:
            # Get input from user
            #start_time_str = input("Enter start time from 8 am (HH:MM:SS AM/PM): ")
            end_time_str = input("Enter end time from 8 am (HH:MM:SS AM/PM) to display packages based on time {special packages duplicated}{enter -1 to exit}: ")

            # Convert strings to datetime objects
            #start_time = datetime.strptime(start_time_str, "%I:%M:%S %p")
            if end_time_str != "-1":
                end_time = datetime.strptime(end_time_str, "%I:%M:%S %p")


            else:
                print("Exiting to go the next menu option")
                break




           # marker = False

            #if end_time < 10.08:
            #    marker = True



            # Filter packages based on delivery time
            for package_info in sorted_package_times:
                # Extract delivery time using string manipulation
                delivery_time_str = package_info.split("Delivery Time: ")[1].split(",")[0].strip()
                delivery_time = datetime.strptime(delivery_time_str, "%I:%M:%S %p")

                if "(0" not in package_info:
                    # Check if the delivery time is within range
                    if delivery_time <= end_time:
                        print(package_info)


                    else:
                            if "Package(9" in package_info and datetime.strptime("10:20:00 AM", "%I:%M:%S %p")>end_time:
                                package_info = package_info.replace("410 S. State St.", "300 State St	Salt Lake City	UT	84103")
                             #   print(f"{package_info} -> Address 300 State St	Salt Lake City	UT	84103")


                            if "Package(6" in package_info and datetime.strptime("9:37:00 AM", "%I:%M:%S %p") <= end_time:
                                package_info = package_info.replace("delivered",      "In Route")
                                print(f"{package_info}")
                                continue

                            elif "Package(6" in package_info and datetime.strptime("9:05:00 AM", "%I:%M:%S %p") <= end_time and end_time < datetime.strptime("9:37:00 AM", "%I:%M:%S %p"):
                                package_info = package_info.replace("delivered",      "In Hub")
                                print(f"{package_info}")
                                continue

                            else:
                                if "Package(6" in package_info:
                                    package_info = package_info.replace("delivered",      "Not Arrived")
                                    print(f"{package_info}")
                                    continue


                            if "Package(25" in package_info and datetime.strptime("9:37:00 AM", "%I:%M:%S %p") <= end_time:
                                package_info = package_info.replace("delivered", "In Route")
                                print(f"{package_info}")
                                continue

                            elif "Package(25" in package_info and datetime.strptime("9:05:00 AM", "%I:%M:%S %p") <= end_time and end_time < datetime.strptime("9:37:00 AM", "%I:%M:%S %p"):
                                package_info = package_info.replace("delivered", "In Hub")
                                print(f"{package_info}")
                                continue

                            else:
                                if "Package(25" in package_info:
                                    package_info = package_info.replace("delivered", "Not Arrived")
                                    print(f"{package_info}")
                                    continue

                            if "Package(28" in package_info and datetime.strptime("9:56:00 AM", "%I:%M:%S %p") <= end_time:
                                package_info = package_info.replace("delivered",      "In Route")
                                print(f"{package_info}")
                                continue

                            elif "Package(28" in package_info and datetime.strptime("9:05:00 AM", "%I:%M:%S %p") <= end_time < datetime.strptime("9:56:00 AM", "%I:%M:%S %p"):
                                package_info = package_info.replace("delivered",      "In Hub")
                                print(f"{package_info}")
                                continue

                            else:
                                if "Package(28" in package_info:
                                    package_info = package_info.replace("delivered", "Not Arrived")
                                    print(f"{package_info}")
                                    continue

                            if "Package(32" in package_info and datetime.strptime("9:56:00 AM", "%I:%M:%S %p") <= end_time:
                                package_info = package_info.replace("delivered", "In Route")
                                print(f"{package_info}")
                                continue

                            elif "Package(32" in package_info and datetime.strptime("9:05:00 AM","%I:%M:%S %p") <= end_time and end_time < datetime.strptime("9:56:00 AM", "%I:%M:%S %p"):
                                package_info = package_info.replace("delivered", "In Hub")
                                print(f"{package_info}")
                                continue

                            else:
                                if "Package(32" in package_info:
                                    package_info = package_info.replace("delivered", "Not Arrived")
                                    print(f"{package_info}")
                                    continue











                            #   print(f"{package_info} -> Address 300 State St	Salt Lake City	UT	84103")

                            if "Truck 3" in package_info and datetime.strptime("9:56:00 AM", "%I:%M:%S %p")<=end_time:
                                package_info = package_info.replace("delivered", "In Route")
                                print(f"{package_info}")


                            elif "Truck 3" in package_info and datetime.strptime("9:56:00 AM", "%I:%M:%S %p")>end_time:
                                package_info = package_info.replace("delivered", "In Hub")
                                print(f"{package_info}")
                            else:
                                package_info = package_info.replace("delivered", "In Route")
                                print(f"{package_info}")



        while store != "-1":
             print("Enter package id and enter (-1) to go to the next menu option")
             store = input()

             for val in sorted_package_times:
                if f"Package({store}," in val:
                   print(val)








#  self.truck3.optimal_routep1
      #  self.truck3.min_distancep1
      #  self.truck3.d_listp1

      #  self.truck3.optimal_routep2
       # self.truck3.min_distancep2
      #  self.truck3.d_listp2

       # self.truck2.perform_brute_force_for_truck(self.truck2.current_packages)

       # print(" ")

      #  self.truck3.perform_brute_force_for_truck(self.truck3.current_packages)




# Create an instance of DeliveryManager and run the main method
if __name__ == "__main__":
    tester = DeliveryManager()
    tester.main()
