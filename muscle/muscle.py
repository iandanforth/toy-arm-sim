import numpy as np

class Muscle(object):

    # motor_units - a list of ints representing fiber counts per motor unit
    def __init__(self, motor_units):

        self.motor_units = motor_units
        
        # Divide our fibers into motor units
        self.motor_unit_count = len(self.motor_units)
        self.activations = None
        self.forces = None

    # activations - an array of floats, one per motor unit
    # returns the force produced by the muscle
    def update(self, activations):
        self.set_activations(activations)
        return self.get_force()

    # activations - an ndarray
    def set_activations(self, activations):
        self.activations = activations

    def get_force(self):
        # Force is equal to the number of fibers * activation for the motor unit
        forces = self.motor_units * self.activations
        total_force = sum(forces)
        return total_force

    def get_motor_unit_count(self):
        return self.motor_unit_count

    def get_activations(self):
        if not self.activations:
            self.activations = np.zeros(self.motor_unit_count)
        return self.activations
