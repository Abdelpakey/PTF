import random
import numpy as np
import matplotlib.pyplot as plt

n_samples = 200
b = 5
# set this to 1 to use the built in triangular distribution generator in Python random module
use_builtin_generator = 0

distr_limit = np.sqrt(6) * b
random.seed()

samples = np.zeros([n_samples, 1])

for i in xrange(n_samples):
    u = random.random()
    if use_builtin_generator:
        x = random.triangular(-distr_limit, distr_limit, 0)
    else:
        if u < 0.5:
            x = 2 * b * np.sqrt(3 * u) - distr_limit
        else:
            x = distr_limit - 2 * b * np.sqrt(3 * (1 - u))

    samples[i] = x

# sample_hist = np.histogram(samples, bins=10)
plt.hist(samples, bins=10)
plt.title("Triangular Distribution Histogram with {:d} samples".format(n_samples))
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid()
plt.show()


