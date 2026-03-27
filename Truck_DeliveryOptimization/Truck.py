#from DeliveryManager import DeliveryManager
#import itertools
#import numpy as np

class Truck:


#initialzie attributes for the Truck Objects
    def __init__(self, truck_id, package_list, distance_matrix_np):

        self.truck_id = truck_id

        self.package_list = package_list

        self.unique_package_groups = None

        self.distance_traversed = 0

        self.distance_matrix_np = distance_matrix_np

        self.capacity = 16
        self.current_packages = []
        self.current_route = []

        self.optimal_routep1 = None
        self.min_distancep1 = None
        self.d_listp1 = None

        self.optimal_routep2 = None
        self.min_distancep2 = None
        self.d_listp2 = None

    def perform_brute_force_for_truck(self, truck_packages):
        # Split into groups of 8
        if self.truck_id == 2:
            truck_packages.insert(0, truck_packages.pop(truck_packages.index(39)))
            truck_packages.insert(0, truck_packages.pop(truck_packages.index(13)))
            truck_packages.insert(0, truck_packages.pop(truck_packages.index(30)))
            truck_packages.insert(0, truck_packages.pop(truck_packages.index(37)))
            truck_packages.insert(0, truck_packages.pop(truck_packages.index(19)))


        groups = [truck_packages[i:i + 8] for i in range(0, len(truck_packages), 8)]
        optimal_routes = []
        #print(groups)
        counter = 0
        if self.truck_id == 2:
            groups = groups[::-1]

        for group in groups:
            if counter == 0:
                self.optimal_routep1,self.min_distancep1, self.d_listp1 = self.brute_force_optimal_route(group, self.distance_matrix_np,counter)  # Call your brute-force method
            if counter == 1:
                self.optimal_routep2,self.min_distancep2, self.d_listp2 = self.brute_force_optimal_route(group, self.distance_matrix_np,counter)  # Call your brute-force method

            counter = counter + 1



        # Optionally: Combine routes in an efficient order or directly return optimal_routes
        return optimal_routes

    @staticmethod
    def permutations(iterable, r=None):
    # permutations('ABCD', 2) → AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) → 012 021 102 120 201 210

        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        if r > n:
            return

        indices = list(range(n))
        cycles = list(range(n, n - r, -1))
        yield tuple(pool[i] for i in indices[:r])

        while n:
            for i in reversed(range(r)):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i + 1:] + indices[i:i + 1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    yield tuple(pool[i] for i in indices[:r])
                    break
            else:
                return
    def brute_force_optimal_route(self, packages, distance_matrix_np, counter):
        """
        Finds the optimal route for a set of locations by brute force.

        Parameters:
            locations (li st): List of location indices to visit.
            distance_matrix (2D numpy array): Adjacency matrix with distances between locations.

        Returns:
            optimal_route (tuple): The route with the minimum total distance.
            min_distance (float): The total distance for the optimal route.
        """
        min_distance = float('inf')
        optimal_route = None
        d_list = None

        node_list = []
        mapped_list = []
        #mapped_list = (package, location)
        for x in packages:
         node_list.append(self.package_list[x]["matrix_index"] + 1)
         mapped_list.append([x, self.package_list[x]["matrix_index"] + 1])

        if self.truck_id == 1 and counter == 1:
         node_list.append(0)
         mapped_list.append(["Hub2", 0])

        route_list = []

        # Generate all possible permutations of the route
        for route in Truck.permutations(mapped_list):
            # Calculate the total distance of this route
            route_list = list(route)
            distance_list = []
            distance = 0


            if counter == 0:
                route_list.insert(0, ["Hub", 0])
            if counter == 1 or self.truck_id == 3:
                route_list.insert(len(route_list),["Hub", 0])
            #print(route_list)
            if self.truck_id == 1 and counter==1:
                store = route_list.index(["Hub2", 0])
                #print(store)


            if self.truck_id == 1 and counter == 1:
                special1 = 0
                special2 = 0
                for i in range(len(route_list) - 1):

                    if route_list[i][0] == 25:
                        special1 = i
                    if route_list[i][0] == 6:
                        special2 = i
            truck3_bool = False
            if self.truck_id == 3:
                if route_list[1][0] == 31:
                    truck3_bool = True


            #  (package, location)
            for i in range(len(route_list)-1):
                start, end = route_list[i][1], route_list[i + 1][1]

                #print(route_list[i][0])

                optimal_position = False
                #distance_threshold = False

                if distance_matrix_np[start][end] > 0:
                    distance += distance_matrix_np[start][end]
                    distance_list.append(distance_matrix_np[start][end])
                else:
                    distance += distance_matrix_np[end][start]
                    distance_list.append(distance_matrix_np[end][start])



                if self.truck_id == 1 and counter == 1:
                    if special1 > store and special2 > store and store<=6:
                        optimal_position = True

                    if i==len(route_list) - 2:
                        if optimal_position == True and distance < min_distance:

                            min_distance = distance
                            optimal_route = route_list
                            d_list = distance_list
                            self.distance_traversed = min_distance

                elif self.truck_id == 3:
                    if  i==len(route_list) - 2 and distance < min_distance and truck3_bool == True:
                        #print("here")
                        min_distance = distance
                        optimal_route = route_list
                        d_list = distance_list
                        self.distance_traversed = min_distance

                else:
            # Update minimum distance and optimal route if a shorter route is found
                    if  i==len(route_list) - 2 and distance < min_distance:
                        #print("here")
                        min_distance = distance
                        optimal_route = route_list
                        d_list = distance_list
                        self.distance_traversed = min_distance


        print(optimal_route)
        print(min_distance)
        print(d_list)

        return optimal_route, min_distance, d_list



    def assign_packages2(self): #Assigns the packages to the trucks

        truck_2_specific = [3, 18, 36, 38, 5, 37, 30] #added in 30 leftover
        #truck_3_specific = [6, 8, 9, 30, 28, 31, 32, 25, 26] #8,9,28

        special_packages = [13, 14, 15, 16, 19, 34, 39, 20, 21]

        truck_3_specific = [8, 9, 28, 32, 31]

        truck_1_specific = []  #truck 1 holds all the other priority packages


    # Add special packages to Truck 2’s list
        truck_2_specific += special_packages

        priority_groupsind = [0, 5, 6, 7, 11, 12, 13, 17, 21, 24]

    # Define unique package groups based on locations
        unique_package_groups = [
        [1],  # 195 W Oakland Ave          #* 0
        [2, 33],  # 2530 S 500 E
        [3],  # 233 Canyon Rd
        [4, 40],  # 380 W 2880 S
        [5, 37, 38],  # 410 S State St
        [6],  # 3060 Lester St             #* 5
        [7, 29],  # 1330 2100 S            #* 6
        [8, 9, 30],  # 300 State St        #* 7
        [10],  # 600 E 900 South
        [11],  # 2600 Taylorsville Blvd
        [12],  # 3575 W Valley Central Station
        [13, 39],  # 2010 W 500 S           #* 11
        [14],  # 4300 S 1300 E              #* 12
        [15, 16, 34],  # 4580 S 2300 E      #* 13
        [17],  # 3148 S 1100 W
        [18],  # 1488 4800 S
        [19],  # 177 W Price Ave
        [20, 21],  # 3595 Main St           #* 17
        [22],  # 6351 South 900 East
        [23],  # 5100 South 2700 West
        [24],  # 5025 State St
        [25, 26],  # 5383 South 900 East #104 #* 21
        [27, 35],  # 1060 Dalton Ave S
        [28],  # 2835 Main St
        [31, 32],  # 3365 S 900 W          #* 24
        [36]  # 2300 Parkway Blvd
    ]

    # Aggregate all assigned packages for Truck 2 and Truck 3
        current = truck_2_specific + truck_3_specific

        truck_1_specific = []

        for group in priority_groupsind:
            if not any(pkg in current for pkg in unique_package_groups[group]):
                truck_1_specific.extend(unique_package_groups[group])
              #  print(truck_1_specific)

        #current = truck_2_specific + truck_3_specific

        temp = current + truck_1_specific
       # current = current + truck_1_specific
    # Step 2: Filter out any groups containing packages already assigned to Truck 2 or Truck 3

        for group in unique_package_groups:
               if not any(pkg in temp for pkg in group):  # Exclude packages already in Truck 2 or Truck 3
                 if(len(truck_1_specific) + len(group)<=16):
                   truck_1_specific.extend(group)

        current = current + truck_1_specific

        for group in unique_package_groups:
            if not any(pkg in current for pkg in group):  # Exclude packages already in Truck 2 or Truck 3
                if (len(truck_3_specific) + len(group) <= 8):
                 truck_3_specific.extend(group)




    # Step 3: Assign packages to each truck
        if self.truck_id == 1:
            self.current_packages = truck_1_specific
        elif self.truck_id == 2:
            self.current_packages = truck_2_specific
        elif self.truck_id == 3:
            self.current_packages = truck_3_specific


    def assign_packages(self):
#special packages adds in
        special_packages = [13, 14, 15, 16, 19, 20]
        counts = 0
        for x in special_packages:
            store2 = self.package_list[x]["matrix_index"]
            temp2 = (self.labels)[store2]
            if temp2 ==1:
                counts = counts + 1
        if counts>= 3:
            for x in special_packages:
                if self.truck_id == 1:
                    #self.current_packages.add(x)
                    if (self.capacity > 0 and x not in self.current_packages): #logic to add packages
                        factor = len(self.current_packages) + 1
                        self.current_packages.append(x)
                        self.current_packages.extend(
                            [elem for elem in self.package_info[x]["duplicates"] if elem not in self.current_packages])
                        factor = len(self.current_packages) - factor
                        self.capacity = self.capacity - factor

        else:
            for x in special_packages:
                if self.truck_id == 2:
                    if(self.capacity>0 and x not in self.current_packages):
                        factor = len(self.current_packages) + 1
                        self.current_packages.append(x)
                        self.current_packages.extend(
                        [elem for elem in self.package_info[x]["duplicates"] if elem not in self.current_packages])
                        factor = len(self.current_packages) - factor
                        self.capacity = self.capacity - factor

  #packages exclusive truck 2 added
        package_truck2 = [3, 18, 36, 38]
        if self.truck_id == 2:
            for x in package_truck2:  # only 2 packages
                #self.current_packages.add(x)
               # self.capacity = self.capacity - 1
                if (self.capacity > 0 and x not in self.current_packages): #logic to add packages
                    factor = len(self.current_packages) + 1
                    self.current_packages.append(x)
                    self.current_packages.extend(
                        [elem for elem in self.package_info[x]["duplicates"] if elem not in self.current_packages])
                    factor = len(self.current_packages) - factor
                    self.capacity = self.capacity - factor

    # packages exclusive truck 3 added
            package_truck3 = [6, 9, 25, 28, 32]
            if self.truck_id == 3:
                for x in package_truck3:
                    if(self.capacity>0 and x not in self.current_packages):
                        factor = len(self.current_packages) + 1
                        self.current_packages.append(x)
                        self.current_packages.extend([elem for elem in self.package_info[x]['duplicates'] if elem not in self.current_packages])
                        factor = len(self.current_packages) - factor
                        self.capacity = self.capacity - factor

  #   self.current_packages = self.current_packages + z
                      #  z = self.package_info[x]

        #fill all the remaining packages
        priority_packages = [1, 6, 13, 14, 15, 16, 19, 20, 25, 28, 30, 34, 37, 38, 40]
        for package_id in range(1,41):
           if package_id not in self.current_packages:
                store = self.package_list[package_id]["matrix_index"]
               # if package_id == 22:
                #    store = store-1
                temp = (self.labels)[store]




                if self.truck_id == 1:
                    if temp == 1 and self.capacity > 0 and package_id not in self.current_packages:
                        #self.current_packages.add(package_id)
                       # self.capacity = self.capacity -1
                        factor = len(self.current_packages) + 1
                        self.current_packages.append(package_id)
                        self.current_packages.extend(
                            [elem for elem in self.package_info[package_id]['duplicates'] if elem not in self.current_packages])
                        factor = len(self.current_packages) - factor
                        self.capacity = self.capacity - factor

                if self.truck_id == 2:
                    #if package_id == 3 or package_id == 18 or package_id == 36 or package_id == 38: #only 2 packages
                    #    self.current_packages.add(package_id)
                    #    self.capacity = self.capacity - 1
                    #    break
                    if temp == 2 and self.capacity > 0 and package_id not in self.current_packages:
                        #self.current_packages.add(package_id)
                        #self.capacity = self.capacity - 1
                        factor = len(self.current_packages) + 1
                        self.current_packages.append(package_id)
                        self.current_packages.extend(
                            [elem for elem in self.package_info[package_id]['duplicates'] if elem not in self.current_packages])
                        factor = len(self.current_packages) - factor
                        self.capacity = self.capacity - factor

               # if self.truck_id == 3:
                 #   if package_id == 6 or package_id == 9 or package_id == 25 or package_id == 28 or package_id == 32 #only 3 packages
                 #       self.current_packages.add(package_id)
                 #       self.capacity = self.capacity - 1
                #      break
                 #   if temp == 3 and self.capacity > 0:
                   #     self.current_packages.add(package_id)
                   #     self.capacity = self.capacity -1
                       # break

    #def run_brute_force(self, distance_matrix):
    #    self.current_route = brute_force_optimal_route(self.current_packages, distance_matrix)
#marks packages delivered
    def deliver_packages(self):
        for package in self.current_route:
            package.mark_delivered()