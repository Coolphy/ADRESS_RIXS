import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from numpy.random import default_rng


x = np.sin(np.arange(-2 * np.pi, 2 * np.pi, 0.01))
y = np.cos(np.arange(0, 4 * np.pi, 0.01))
correlation = signal.correlate(x, y, mode="full")
lags = signal.correlation_lags(x.size, y.size, mode="full")
lag = lags[np.argmax(correlation)]

plt.plot(x)
plt.plot(y)
plt.plot(lags, correlation / 100)
plt.plot(correlation / 100)
plt.show()
