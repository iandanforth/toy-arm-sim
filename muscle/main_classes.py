from random import randint
from collections import Counter

class Fiber(object):

	def __init__(self, strength, speed):
		self.strength = strength
		self.speed = speed

	def getStrength(self):
		return self.strength

	def setStrength(self, strength):
		if not (0.0 < strength < 1.0):
			raise Exception('Fiber strength must be between 0.0 and 1.0')
		self.strength = strength

class MotorUnit(object):

	def __init__(self, fibers):
		self.fibers = fibers
		self.activation = 0

	def getFiberCount(self):
		return len(self.fibers)

	def setActivation(self, activation):
		self.activation = activation

	def get_force(self):
		return sum([f.getStrength() for f in self.fibers]) * self.activation


class Muscle(object):

	# fibers - an array of Fiber objects
	# innervationRatio - an int (typically >> 1)
	# spindle_callback - a function which takes feedback from muscle spindles
	# golgi_callback - a function which takes feedback from golgi organs
	def __init__(self, fibers, innervationRatio, spindle_callback, golgi_callback):

		self.fibers = fibers
		
		# Divide our fibers into motor units
		self.motorUnitCount = len(self.fibers) / innervationRatio
		self.motorUnits = []
		for i in range(self.motorUnitCount):
			start = i * innervationRatio
			stop = start + self.motorUnitCount
			mu = MotorUnit(self.fibers[start:stop])
			self.motorUnits.append(mu)

	def set_activations(self, activations):
		if (len(activations) != self.motorUnitCount):
			print len(activations)
			print self.motorUnitCount
			raise Exception('Activation array must be of same length as fibers array')
		for i, a in enumerate(activations):
			self.motorUnits[i].setActivation(a)

	def getActivations(self):
		return self.activations

	def get_force(self):
		return sum([mu.get_force() for mu in self.motorUnits])

	def get_motor_unit_count(self):
		return self.motorUnitCount


def main():

	# Create all the muscles
	muscles = []
	fiber_total = 0
	motor_unit_total = 0
	for i in range(800):
		fiber_count = randint(1000, 10000)
		fiber_total += fiber_count
		fibers = [Fiber(0.5, 0.5) for _ in range(fiber_count)]
		def spindle():
			pass
		def golgi():
			pass

		innervationRatio = randint(100, 800)
		motor_unit_total += (fiber_count / innervationRatio)
		m = Muscle(fibers, innervationRatio, spindle, golgi)
		muscles.append(m)

	# How many motor units did we just create?
	print fiber_total
	print motor_unit_total

	# Activate all the fibers
	forces = []
	for m in muscles:
		m.set_activations([1 for _ in range(m.get_motor_unit_count())])
		forces.append(m.get_force())



if __name__ == '__main__':
	main()