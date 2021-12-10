import math


def EtoQ(energy):
    qvalue = energy / 1000
    return qvalue


def qTrans(energy, twoTheta):
    qTrans = EtoQ(energy) * math.sin(twoTheta / 180 * math.pi / 2) * 2
    return qTrans


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
    br = 2 * math.pi * a * c * math.sin(beta / 180 * math.pi) / Vol
    cr = 2 * math.pi * a * b * math.sin(gamma / 180 * math.pi) / Vol

    return ar, br, cr


def vectorSum(a, b, gamma):
    sum = math.sqrt(a * a + b * b - 2 * a * b * cos((180 - gamma) / 180 * math.pi))
    return sum


twoTheta = 130
energy = 530

# alpha = 10
# qIn, qOut = project(energy, twoTheta, alpha)

theta = 120
qIn, qOut = thToq(energy, twoTheta, adressTheta(theta, twoTheta))

# qIn = 1
# alpha = qInToth(energy, twoTheta, qIn)

qIn = 1
theta = adressTheta(qInToth(energy, twoTheta, qIn), twoTheta)


lattice = [3.14, 3.14, 3.14, 90, 90, 90]
ar, br, cr = invertedframe(lattice)

# (1,0)
q = qIn / ar

# (1,1)
q = qIn / vectorSum(ar, br, (180 - lattice[5]))
