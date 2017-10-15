import numpy as np

# Returns a sample or samples from a normal distibution centered halfway between start and stop
# e.g. if the range is 100 -> 1000 then the mean of the distribution will be 450
# start - inclusive start value for the range
# stop - inclusive stop value for the range
# std - How many standard deviations should appear within the range
# count - number of samples to return
# round - Whether to return nearest ints or unrounded floats.
# skew - mu offset
def norm_in_range(start, stop, std=4, count=1, round=False, skew=0):
    mu = (stop - start) / 2
    sigma = mu / std # Allow std standard deviations within the range
    vals = []
    for _ in xrange(count):
        picked = False
        while not picked:
            val = sigma * np.random.randn() + (mu + skew)
            if start <= val <= stop:
                if round:
                    val = int(np.round(val))
                vals.append(val)
                picked = True
    return vals

# Returns a sample or samples from the left half of a normal distibution centered on start
# start - inclusive start value for the range
# stop - inclusive stop value for the range
# std - How many standard deviations should appear within the range
# count - number of samples to return
# round - Whether to return nearest ints or unrounded floats.
def half_norm_in_range(start, stop, std=4, count=1, round=False):
    mu = start
    sigma = (stop - start) / std # Allow std standard deviations within the range
    vals = []
    for _ in xrange(count):
        picked = False
        while not picked:
            val = sigma * np.random.randn() + mu
            if val >= start:
                if round:
                    val = int(np.round(val))
                vals.append(val)
                picked = True
    return vals

def gen_motor_units(total_fiber_count, fiber_population_mean, max_innervation_ratio ):
    fiber_pool = total_fiber_count
    scaling_factor = total_fiber_count / fiber_population_mean
    # All muscles follow ~ the same distribution, but with different ranges
    # Small muscles are much more likely to have a smaller max fiber count amongst their motor units
    # Large muscles are more likely to have a larger max fiber count amongst their motor units
    max_mu_fiber_count = max_innervation_ratio * scaling_factor
    motor_units = []
    while fiber_pool > 0:

        fiber_count = half_norm_in_range(5, max_mu_fiber_count, std=3, round=True)[0]
        if fiber_count > fiber_pool:
            motor_units.append(fiber_pool)
        else:
            motor_units.append(fiber_count)

        fiber_pool -= fiber_count

    return motor_units