# %%
from sympy import *

init_printing()

e, theta, two_theta, specular = symbols("e theta two_theta specular", positive=True)

k = e / 1973
k_trans = sqrt(k**2 * (2 - 2 * cos(two_theta)))
delta = specular - theta
k_in_plane = k_trans * sin(delta)
k_out_plane = k_trans * cos(delta)

a, gamma = symbols("a gamma", positive=True)

# (1,0)
ar = 2 * pi / (a * sin(pi - gamma))

# (1,1)
aar = sqrt(ar**2 * (2 - 2 * cos(gamma)))

# (1,0)

# %%
q10 = k_in_plane / ar
simplify(q10)

# %%
q10value = q10.subs(
    [
        (two_theta, 130 / 180 * pi),
        (a, 4.985),
        (gamma, 120 / 180 * pi),
        (e, 708),
        # (specular, 65 / 180 * pi),
        # (theta, 40),
    ]
)

print(simplify(q10value.evalf(4)))

q01value = q10.subs(
    [
        (two_theta, 130 / 180 * pi),
        (a, 4.049),
        (gamma, 90 / 180 * pi),
        (e, 708),
        (specular, 65 / 180 * pi),
        # (theta, 40),
    ]
)

print(simplify(q01value.evalf(4)))

# simplify(q01value)
# %%
# (1,1)

q11 = k_in_plane / aar
simplify(q11)

# %%
q11value = q11.subs(
    [
        (two_theta, 130 / 180 * pi),
        (a, 3.14),
        (gamma, 90 / 180 * pi),
        (e, 530),
        (specular, 65 / 180 * pi),
        # (theta, 40),
    ]
)

print(simplify(q11value.evalf(4)))


# %%
import matplotlib.pyplot as plt
import numpy as np
import math


thetaarray = np.arange(0, 130, 1) * pi / 180
r = np.ones(130) * 0.4469

x = 0.4469 * np.sin(65.0 * math.pi / 180.0 - thetaarray.astype(float))
y = 0.4192 * np.cos(65.0 * math.pi / 180.0 - thetaarray.astype(float))

rect = [0.1, 0.1, 0.8, 0.8]

fig = plt.figure()

axs = fig.add_axes(rect)
# axp = fig.add_axes(axs.get_position().bounds, polar=True, frameon=False)
fig.gca().set_aspect(1.066)
axs.plot(x, y)
axs.set_xlim([-0.5, 0.5])
axs.set_ylim([0, 0.5])
axs.grid()
axs.set_xlabel("[H, 0 ,0 ]")
axs.set_ylabel("[0, 0 ,L ]")

# %%
