# %%
import math
import numpy as np


def EtoQ(energy):
    qvalue = energy / 1973
    return qvalue


def qTrans(energy, twoTheta):
    qTrans = EtoQ(energy) * math.sin(twoTheta / 180 * math.pi / 2) * 2
    return qTrans


def adressTheta(theta, twoTheta):
    alpha = twoTheta - theta
    return alpha


def calVolume(a, b, c, alpha, beta, gamma):

    Volume = (
        a
        * b
        * c
        * math.sqrt(
            1
            - math.cos(alpha / 180 * math.pi) * math.cos(alpha / 180 * math.pi)
            - math.cos(beta / 180 * math.pi) * math.cos(beta / 180 * math.pi)
            - math.cos(gamma / 180 * math.pi) * math.cos(gamma / 180 * math.pi)
            + 2
            * math.cos(alpha / 180 * math.pi)
            * math.cos(beta / 180 * math.pi)
            * math.cos(gamma / 180 * math.pi)
        )
    )
    return Volume


def invertedframe(latticeConstant):
    [a, b, c, alpha, beta, gamma] = latticeConstant
    Vol = calVolume(a, b, c, alpha, beta, gamma)
    ar = 2 * math.pi * b * c * math.sin(alpha / 180 * math.pi) / Vol
    br = 2 * math.pi * c * a * math.sin(beta / 180 * math.pi) / Vol
    cr = 2 * math.pi * a * b * math.sin(gamma / 180 * math.pi) / Vol

    return ar, br, cr


def thToq(energy, twoTheta, alpha):
    qParallel = qTrans(energy, twoTheta) * math.cos(
        (alpha + (180 - twoTheta) / 2) / 180 * math.pi
    )
    qPerpendicular = qTrans(energy, twoTheta) * math.sin(
        (alpha + (180 - twoTheta) / 2) / 180 * math.pi
    )
    return qParallel, qPerpendicular


def qInToth(energy, twoTheta, qIn):

    alpha = (
        math.acos(qIn / qTrans(energy, twoTheta)) / math.pi * 180 - (180 - twoTheta) / 2
    )
    return alpha


def vectorSum(a, b, gamma):
    sum = math.sqrt(a * a + b * b - 2 * a * b * math.cos((180 - gamma) / 180 * math.pi))
    return sum


# %%
twoTheta = 130
energy = 930

lattice = [3.909, 3.494, 12.69, 90, 90, 90]
ar, br, cr = invertedframe(lattice)

# %%
# alpha = 10
# qIn, qOut = project(energy, twoTheta, alpha)

theta = 130
qIn, qOut = thToq(energy, twoTheta, adressTheta(theta, twoTheta))

# (1,0)
q = qIn / ar
print(q)

# (1,1)
q = qIn / vectorSum(ar, br, (180 - lattice[5]))
print(q)

# (H,K)

# %%
# qIn = 1
# alpha = qInToth(energy, twoTheta, qIn)

# (1,0)
q = 0.4
qIn = q * ar
theta = adressTheta(qInToth(energy, twoTheta, qIn), twoTheta)
print(theta)

# (1,1)
q = 0.2
qIn = vectorSum(ar, br, (180 - lattice[5])) * q
theta = adressTheta(qInToth(energy, twoTheta, qIn), twoTheta)
print(theta)

# (H,K)
q = [0.35, 0.35]
qIn = vectorSum(ar * q[0], br * q[1], (180 - lattice[5]))
theta = adressTheta(qInToth(energy, twoTheta, qIn), twoTheta)
print(theta)

# %%
for q in np.linspace(0.45, -0.45, 91):
    qIn = q * ar
    theta = adressTheta(qInToth(energy, twoTheta, qIn), twoTheta)
    print(np.round(q, 3), np.round(theta, 3))

# %%
