# import simpy
# import random
# import unittest

# # Constants
# SIMULATION_TIME = 7 * 24 * 60  # Simulation time in minutes
# AVERAGE_ARRIVAL_TIME = 300  # Average time between vessel arrivals in minutes
# NUM_BERTHS = 2  # Number of available berths
# NUM_QUAY_CRANES = 2  # Number of quay cranes
# NUM_TRUCKS = 3  # Number of trucks


# # Tried giving name and printing which crane and truck are using the vessle
# # class NamedResource(simpy.Resource):
# #     count = {}
    
# #     def __init__(self, env, capacity, name):
# #         super().__init__(env, capacity)
# #         self.name = f"{name}_{NamedResource.count.get(capacity, 1)}"
# #         NamedResource.count[capacity] = NamedResource.count.get(capacity, 1) + 1
# '''
# Main vessle class
# '''
# class Vessel:
#     def __init__(self, name, containers):
#         self.name = name
#         self.containers = containers

# '''
# Generate vessels with exponential inter-arrival time
# '''
# def vessel_generator(env, vessel_queue, logs):
#     arrival_time = 0
#     counter = 1
#     while True:
#         # Generate a new vessel
#         vessel_name = f"Vessel {counter}"
#         containers = 150
#         vessel = Vessel(vessel_name, containers)
        
#         # Log vessel arrival
#         print(f"{env.now}: {vessel.name} arrives at the terminal")
#         logs.append(f"{env.now}: {vessel.name} arrives at the terminal")
        
#         # Add vessel to the queue
#         yield vessel_queue.put(vessel)
        
#         # Schedule the next vessel arrival
#         inter_arrival_time = random.expovariate(1 / AVERAGE_ARRIVAL_TIME)
#         yield env.timeout(inter_arrival_time)
#         arrival_time += inter_arrival_time
#         counter += 1

# '''
# Generate berth based on available crane and truck
# '''
# def berth(env, vessel_queue, quay_crane, truck_resource, logs):
#     while True:
#         # Wait for a vessel to arrive
#         vessel = yield vessel_queue.get()
        
#         # Log vessel berthing
#         print(f"{env.now}: {vessel.name} starts berthing")
#         logs.append(f"{env.now}: {vessel.name} starts berthing")
        
#         # Use a quay crane to unload containers
#         with quay_crane.request() as crane_request:
#             yield crane_request
#             while vessel.containers > 0:
#                 # Move one container from the vessel to a truck
#                 yield env.timeout(3)  # Time taken to move one container
#                 vessel.containers -= 1
                
#                 # Use a truck to transport the container to the yard block
#                 with truck_resource.request() as truck_request:
#                     yield truck_request
#                     yield env.timeout(6)  # Time taken to transport the container
                    
#                     # Log container movement
#                     print(f"{env.now}: {vessel.name} container {vessel.containers} moved to yard block")
#                     logs.append(f"{env.now}: {vessel.name} container {vessel.containers} moved to yard block")
        
#         # Log vessel departure
#         print(f"{env.now}: {vessel.name} leaves the terminal")
#         logs.append(f"{env.now}: {vessel.name} leaves the terminal")
        
# '''
# Main driver code running the simulation and checking test cases
# '''
# class SimulationTestCase(unittest.TestCase):

#     def setUp(self):
#         self.env = simpy.Environment()
#         self.vessel_queue = simpy.Store(self.env)
#         self.quay_crane = simpy.Resource(self.env, capacity=NUM_QUAY_CRANES)
#         self.truck_resource = simpy.Resource(self.env, capacity=NUM_TRUCKS)
#         self.logs = [] 

#     def tearDown(self):
#         self.env = None
#         self.vessel_queue = None
#         self.quay_crane = None
#         self.truck_resource = None
#         self.logs = None

#     def test_simulation(self):
#         self.env.process(vessel_generator(self.env, self.vessel_queue,self.logs))
#         for _ in range(NUM_BERTHS):
#             self.env.process(berth(self.env, self.vessel_queue, self.quay_crane, self.truck_resource, self.logs))

#         self.env.run(until=SIMULATION_TIME)

#         for log1 in self.logs:
#             print(log1)
#         # Assertion for vessel arrivals
#         expected_vessels = SIMULATION_TIME // AVERAGE_ARRIVAL_TIME
#         self.assertGreaterEqual(expected_vessels, len(self.vessel_queue.items), "Number of vessels less than the expected value")

#         # Assertion for vessel berthing
#         berthing_logs = [
#             log for log in self.logs if log.endswith("starts berthing")
#         ]
#         self.assertLessEqual(NUM_BERTHS, len(berthing_logs), "Number of berthing events less than NUM_BERTHS  value")

#         # Assertion for container movements
#         container_movement_logs = [
#             log for log in self.logs if "container" in log
#         ]
#         expected_containers_moved = expected_vessels * 150
#         self.assertGreaterEqual(expected_containers_moved, len(container_movement_logs), "Number of container in waiting")

#         # Assertion for resource usage
#         self.assertGreaterEqual(len(self.vessel_queue.items), NUM_BERTHS, "Number of vessels in queue less than available berths")
#         self.assertGreaterEqual(len(self.quay_crane.users), NUM_QUAY_CRANES, "Number of quay cranes in use less than the available capacity")
#         self.assertLessEqual(len(self.truck_resource.users), NUM_TRUCKS, "Number of trucks in use less than the available capacity")

#         # Assertion for simulation completion
#         self.assertEqual(self.env.now, SIMULATION_TIME, "Simulation did not complete within the specified time")


        

# if __name__ == '__main__':
#     unittest.main()
