#! /Users/iandanforth/tensorflow/bin/python
from random import randint
from collections import Counter
try:
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go
except:
    pass
import numpy as np
from muscle import Muscle
from helpers import (norm_in_range, gen_motor_units)
np.random.seed(11311)
DEBUG = False

def main():

    # Parameters
    muscle_count = 100 # How many muscles to create
    min_innervation_ratio = 5
    max_innervation_ratio = 2000 # This is a probabalistic set point, not a hard max
    min_fiber_count = 1000
    max_fiber_count = 1500000
    skew = -500000

    # Create all the fibers in the body
    # We want an aproximately normal distribution of fiber counts across all muscles
    # We skew that distribution toward smaller fiber counts as is found in the human body
    fiber_counts_by_muscle = norm_in_range(
        min_fiber_count,
        max_fiber_count, 
        std=3, 
        count=muscle_count, 
        round=True, 
        skew=skew
    )
    fiber_counts_by_muscle = sorted(fiber_counts_by_muscle)
    fiber_population_mean = np.mean(fiber_counts_by_muscle) # ~300,000

    if plotly and DEBUG:
        data = [go.Histogram(x=fiber_counts_by_muscle)]
        plotly.offline.plot(data)


    ##############################################################################
    # One muscle
    f_count = norm_in_range(
        min_fiber_count,
        max_fiber_count, 
        3, 
        round=True, 
        skew=skew
    )
    f_count = f_count[0]
    print "Number of fibers: ", f_count

    motor_units = gen_motor_units(f_count, fiber_population_mean, max_innervation_ratio)
    print "Number of Motor Units: ", len(motor_units)
    print "Innervation Number: ", f_count / len(motor_units)
    m = Muscle(motor_units)
    activations = m.get_activations()

    print m.get_force()

    ##############################################################################
    # All muscles
    muscles = []
    for fiber_count in fiber_counts_by_muscle:
        # For each muscle we want to group muscle fibers into motor units
        # Each motor unit is an int representing the number of fibers the unit innervates
        motor_units = gen_motor_units(fiber_count, fiber_population_mean, max_innervation_ratio)

        m = Muscle(motor_units)
        muscles.append(m)


    # Activate all the muscles
    forces = []

    for m in muscles:
        l = m.get_motor_unit_count()
        m.set_activations(np.random.rand(l))
        force = m.get_force()
        forces.append(force)

    print sorted(forces)



if __name__ == '__main__':
    main()