# %%
import numpy as np
import matplotlib.pyplot as plt

from lmfit import Minimizer, Parameters, report_fit
from lmfit import Model
from lmfit.models import GaussianModel, LinearModel

# %%
def init_multi_peaks(x, y, peak_number=1, plot=True):

    linear1 = LinearModel(prefix="b_")
    pars = linear1.guess(y, x=x)

    gaussian = {}

    mod = linear1

    for i in range(peak_number):

        gaussian[i] = GaussianModel(prefix=f"p{i}_")
        pars.update(gaussian[i].make_params())

        mod = mod + gaussian[i]

    init = mod.eval(pars, x=x)

    if plot == True:
        fig, axes = plt.subplots()
        axes.plot(x, y, "o")
        axes.plot(x, init, "-")

    return pars


def fit_multi_peaks(x, y, peak_number=1, plot=True, init=None):

    linear1 = LinearModel(prefix="b_")
    pars = linear1.guess(y, x=x)

    gaussian = {}

    mod = linear1

    for i in range(peak_number):

        gaussian[i] = GaussianModel(prefix=f"p{i}_")

        if init is None:
            pars.update(gaussian[i].make_params())

        mod = mod + gaussian[i]

    if init is not None:
        pars.update(init)

    out = mod.fit(y, pars, x=x)

    errs = {}
    for i, key in enumerate(out.best_values):
        errs[key] = np.sqrt(np.diag(out.covar))[i]

    if plot is True:
        fig, axes = plt.subplots()
        axes.plot(x, y, "o")
        axes.plot(x, out.best_fit, "-")

        comps = out.eval_components(x=x)

        for key in comps:
            axes.plot(x, comps[key], "--")

    return out.best_values, errs


# %%
def try_fit(x, y):
    init_pars = init_multi_peaks(x, y, peak_number=5)

    for key in init_pars:
        print(key)

    init_pars["p0_center"].set(value=-1.01)
    init_pars["p0_sigma"].set(value=0.14)
    init_pars["p0_amplitude"].set(value=40)
    init_pars["p1_center"].set(value=-1.34)
    init_pars["p1_sigma"].set(value=0.14)
    init_pars["p1_amplitude"].set(value=40)
    init_pars["p2_center"].set(value=-1.91)
    init_pars["p2_sigma"].set(value=0.14)
    init_pars["p2_amplitude"].set(value=40)
    init_pars["p3_center"].set(value=-2.4)
    init_pars["p3_sigma"].set(value=0.14)
    init_pars["p3_amplitude"].set(value=40)
    init_pars["p4_center"].set(value=-3.16)
    init_pars["p4_sigma"].set(value=0.14)
    init_pars["p4_amplitude"].set(value=40)

    fits, errs = fit_multi_peaks(x, y, peak_number=5, init=init_pars)

    return fits, errs


# %%
if __name__ == "__main__":
    X = np.array([])
    Y = np.array([])
    try_fit(X[(X > -4) & (X < -0.5)], Y[(X > -4) & (X < -0.5)])
