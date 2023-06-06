import sys
import os

# Add the simulation directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
import simpy
# from models.vessle import Vessel
from simulation.resources.named_resource import NamedResource
from simulation.resources.config import conf
from simulation.processes.simulation_processes import vessel_generator, berth

class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        self.env = simpy.Environment()
        self.vessel_queue = simpy.Store(self.env)
        self.quay_crane = NamedResource(self.env, capacity=2, name="Quay Crane")
        self.truck_resource = NamedResource(self.env, capacity=3, name="Truck")
        self.logs = []

    def tearDown(self):
        self.env = None
        self.vessel_queue = None
        self.quay_crane = None
        self.truck_resource = None
        self.logs = None

    def test_simulation(self):
        self.env.process(vessel_generator(self.env, self.vessel_queue, self.logs))
        self.env.process(berth(self.env, self.vessel_queue, self.quay_crane, self.truck_resource, self.logs))

        # Run the simulation for a certain time
        # self.env.run(until=7 * 24 * 60)
        self.env.run(until=10000)


        # Assert simulation results
        self.assertGreaterEqual(len(self.logs), 8)  # Expected number of events

        # Assert specific event logs
        self.assertIn("Vessel 1 arrives at the terminal", self.logs)
        self.assertIn("Vessel 1 starts berthing", self.logs)
        self.assertIn("Vessel 1 leaves the terminal", self.logs)


if __name__ == "__main__":
    unittest.main()
