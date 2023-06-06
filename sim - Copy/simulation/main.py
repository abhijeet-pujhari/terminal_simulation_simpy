import simpy
import random
from resources.config import conf
from resources.named_resource import NamedResource
from processes.simulation_processes import vessel_generator, berth



def run_simulation(simulation_time):
    # Create environment
    env = simpy.Environment()

    vessel_queue = simpy.Store(env)
    quay_crane = NamedResource(env, capacity=2, name="Quay Crane")
    truck_resource = NamedResource(env, capacity=3, name="Truck")
    logs = []

    # Start vessel generator process
    env.process(vessel_generator(env, vessel_queue, logs))

    # Start berth processes
    for _ in range(conf.get("NUM_BERTHS")):
        env.process(berth(env, vessel_queue, quay_crane, truck_resource, logs))

    # Run the simulation
    env.run(until=simulation_time)

# Run the simulation
run_simulation(conf.get("SIMULATION_TIME"))
