from random import randint
from collections import Counter
import numpy as np
from scipy.signal import triang

# class Fiber(object):

# 	def __init__(self, strength, speed):
# 		self.strength = strength
# 		self.speed = speed

# 	def getStrength(self):
# 		return self.strength

# 	def setStrength(self, strength):
# 		if not (0.0 < strength < 1.0):
# 			raise Exception('Fiber strength must be between 0.0 and 1.0')
# 		self.strength = strength

# class MotorUnit(object):

# 	def __init__(self, fibers):
# 		self.fibers = fibers
# 		self.activation = 0

# 	def getFiberCount(self):
# 		return len(self.fibers)

# 	def setActivation(self, activation):
# 		self.activation = activation

# 	def getForce(self):
# 		return sum([f[0] for f in self.fibers]) * self.activation


class Muscle(object):

	# fibers - an array of tuples (strength, speed)
	# innervation_ratio - an int (typically >> 1)
	# spindleCallback - a function which takes feedback from muscle spindles
	# golgiCallback - a function which takes feedback from golgi organs
	def __init__(self, fibers, innervation_ratio, spindleCallback, golgiCallback):

		self.fibers = fibers
		self.fiber_strengths = np.array([f[0] for f in self.fibers])
		self.fiber_count = len(self.fibers)
		self.innervation_ratio = innervation_ratio
		
		# Divide our fibers into motor units
		self.motor_unit_count = self.fiber_count / self.innervation_ratio
		self.extra_fiber_count = self.fiber_count % self.innervation_ratio
		self.activations = None

		# The set of innervation filters across all fibers
		self.innervation_filter = []
		# For each motor unit
		for i in range(self.motor_unit_count - 1):
			
			# A triangle filter around the center of the unit
			# This will simulate the diminishing strength a signal has on fibers distant from
			# a motor neuron.
			f = triang(innervation_ratio)
			self.innervation_filter.extend(f)

		# Final motor unit picks up any extra fibers
		self.innervation_filter.extend(triang(self.innervation_ratio + self.extra_fiber_count))
		self.innervation_filter = self.innervation_filter


	def setActivations(self, activations):
		self.activations = activations

	def getActivations(self):
		return self.activations

	def getForce(self):
		print len(self.fiber_strengths)
		print len(self.innervation_filter)
		print len(self.activations)
		
		quit()
		return sum(self.fiber_strengths * (self.innervation_filter * self.activations))

	def getMotorUnitCount(self):
		return self.motor_unit_count


def main():

	# Create all the muscles
	muscles = []
	for i in range(800):
		fibers = [(0.5, 0.5) for _ in range(randint(1000, 100000))]
		def spindle():
			pass
		def golgi():
			pass

		innervation_ratio = randint(100, 800)
		m = Muscle(fibers, innervation_ratio, spindle, golgi)
		muscles.append(m)

	# How many motor units did we just create?
	print sum([m.getMotorUnitCount() for m in muscles])

	# Activate all the fibers
	forces = []
	for m in muscles:
		m.setActivations([1 for _ in range(m.getMotorUnitCount())])
		forces.append(m.getForce())

	print Counter(forces)



if __name__ == '__main__':
	main()