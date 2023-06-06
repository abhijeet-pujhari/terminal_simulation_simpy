import sys
import os

# Add the simulation directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import simpy
import random
from resources.config import conf
from models.vessle import Vessel

def vessel_generator(env, vessel_queue, log):
    # Generate vessels with exponential inter-arrival time
    counter = 1
    while True:
        # Generate a new vessel
        vessel_name = f"Vessel {counter}"
        containers = 150
        vessel = Vessel(vessel_name, containers)

        # Log vessel arrival
        print(f"{env.now}: {vessel.name} arrives at the terminal")
        log.append(f"{vessel.name} arrives at the terminal")

        # Add vessel to the queue
        yield vessel_queue.put(vessel)

        # Schedule the next vessel arrival
        inter_arrival_time = random.expovariate(1 / conf.get("AVERAGE_ARRIVAL_TIME"))
        yield env.timeout(inter_arrival_time)
        counter += 1

def berth(env, vessel_queue, quay_crane, truck_resource, log):
    while True:
        # Wait for a vessel to arrive
        vessel = yield vessel_queue.get()

        # Log vessel berthing
        print(f"{env.now}: {vessel.name} starts berthing")
        log.append(f"{vessel.name} starts berthing")

        # Use a quay crane to unload containers
        with quay_crane.request() as crane_request:
            yield crane_request
            while vessel.containers > 0:
                # Move one container from the vessel to a truck
                yield env.timeout(3)  # Time taken to move one container
                vessel.containers -= 1

                # Use a truck to transport the container to the yard block
                with truck_resource.request() as truck_request:
                    yield truck_request
                    yield env.timeout(6)  # Time taken to transport the container

                    # Log container movement
                    print(f"{env.now}: {vessel.name} container {vessel.containers} moved to yard block")
                    log.append(f"{vessel.name} container {vessel.containers} moved to yard block")

        # Log vessel departure
        print(f"{env.now}: {vessel.name} leaves the terminal")
        log.append(f"{vessel.name} leaves the terminal")
