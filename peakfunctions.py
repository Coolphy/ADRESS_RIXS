import numpy as np


def gauss_norm(x, xc, sigma, area):
    norm = 1.0 / sigma / 2 / np.sqrt(np.pi / 2)
    return area * norm * np.exp(-2 * (x - xc) ** 2 / (sigma * 2) ** 2)


def gaussian_norm(x, xc, fwhm, area):
    norm = 1.0 / fwhm / np.sqrt(np.pi / 4 / np.log(2))
    return area * norm * np.exp(-4 * np.log(2) * (x - xc) ** 2 / fwhm**2)


def gauss_amp(x, xc, sigma, amp):
    return amp * np.exp(-2 * (x - xc) ** 2 / (sigma * 2) ** 2)


def gaussian_amp(x, xc, fwhm, amp):
    return amp * np.exp(-4 * np.log(2) * (x - xc) ** 2 / fwhm**2)


def lorentz_norm(x, xc, fwhm, area):
    return 2 * area / np.pi * fwhm / (4 * (x - xc) ** 2 + fwhm**2)


def lorentz_amp(x, xc, fwhm, amp):
    return amp * fwhm**2 / (4 * (x - xc) ** 2 + fwhm**2)


def Psd_Voigt(x, xc, w, mu, area):
    return area * (
        mu * 2 / np.pi * w / (4 * (x - xc) ** 2 + w**2)
        + (1 - mu)
        * np.sqrt(4 * np.log(2.0))
        / np.sqrt(np.pi)
        / w
        * np.exp(-4 * np.log(2.0) * (x - xc) ** 2 / w**2)
    )


def Psd_Voigt2(x, xc, wl, wg, mu, area):
    return area * (
        mu * 2 / np.pi * wl / (4 * (x - xc) ** 2 + wl**2)
        + (1 - mu)
        * np.sqrt(4 * np.log(2.0))
        / np.sqrt(np.pi)
        / wg
        * np.exp(-4 * np.log(2.0) * (x - xc) ** 2 / wg**2)
    )
