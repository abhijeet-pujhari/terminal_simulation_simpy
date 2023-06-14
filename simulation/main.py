import simpy
import argparse
from resources.config import conf
from resources.named_resource import NamedResource
from processes.simulation_processes import vessel_generator, berth



def run_simulation(simulation_time, quay_crane_arg, truck_resource_arg):
    # Create environment
    env = simpy.Environment()

    vessel_queue = simpy.Store(env)
    quay_crane = NamedResource(env, capacity=quay_crane_arg, name="Quay Crane")
    truck_resource = NamedResource(env, capacity=truck_resource_arg, name="Truck")
    logs = []

    # Start vessel generator process
    env.process(vessel_generator(env, vessel_queue, logs))

    # Start berth processes
    for _ in range(conf.get("NUM_BERTHS")):
        env.process(berth(env, vessel_queue, quay_crane, truck_resource, logs))

    # Run the simulation
    env.run(until=simulation_time)

# Run the simulation
# run_simulation(conf.get("SIMULATION_TIME"))
def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Container Terminal Simulation')

    # Add the 
    parser.add_argument('--time', type=int, default=conf.get('SIMULATION_TIME'),
                        help='time')
    
    parser.add_argument('--trucks', type=int, default=conf.get('NUM_TRUCKS'),
                        help='number of trucks')
    
    parser.add_argument('--cranes', type=int, default=conf.get('NUM_QUAY_CRANES'),
                        help='number of cranes')
    

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the simulation
    run_simulation(args.time, args.trucks, args.cranes)

if __name__ == '__main__':
    main()
