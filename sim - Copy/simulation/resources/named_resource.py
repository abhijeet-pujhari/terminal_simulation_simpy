import simpy

class NamedResource(simpy.Resource):
    count = {}
    
    def __init__(self, env, capacity, name):
        super().__init__(env, capacity)
        self.name = name + f"_{NamedResource.count.get(self.capacity, 1)}"
        NamedResource.count[self.capacity] = NamedResource.count.get(self.capacity, 1) + 1
