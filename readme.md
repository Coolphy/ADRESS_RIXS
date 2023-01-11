```python
import h5py
import numpy as np
from scipy.signal import correlate, correlation_lags

```

```python
xas_dict = {}


def load_xas(scan_number, path=project_path.replace("\\", "/"), base=base_atom):

    global xas_dict
    if scan_number not in xas_dict:
        xas = {}
        data = np.loadtxt(f"{path}/XAS/{base}_{scan_number:04d}.xas", comments="#")
        xas["EN"] = data[:, 0]
        xas["TEY"] = data[:, 1]
        xas["TFY"] = data[:, 2]
        xas["RMU"] = data[:, 3]
        xas_dict[scan_number] = xas
    else:
        xas = xas_dict[scan_number]

    return xas["EN"], xas["TEY"], xas["TFY"], xas["RMU"]

```

```python
rixs_dict = {}


def load_h5(file_name):

    f = h5py.File(file_name, "r")
    ccd = np.array(f["entry"]["analysis"]["spectrum"][()])
    f.close()

    return ccd


def load_ccds(scan_number, path=project_path.replace("\\", "/"), base=base_atom):

    global rixs_dict
    if scan_number not in rixs_dict:
        rixs = {}
        for i in range(1, 4):
            rixs[i] = load_h5(f"{path}/RIXS/{base}_{scan_number:04d}_d{i}.h5")
        rixs_dict[scan_number] = rixs
    else:
        rixs = rixs_dict[scan_number]

    return rixs[1], rixs[2], rixs[3]

```

```python
def x_corr(refData, uncorrData):

    corr = correlate(refData, uncorrData)
    lags = signal.correlation_lags(len(refData), len(uncorrData))
    lag = lags[np.argmax(corr)]
    corrData = np.roll(uncorrData, lag)

    return corrData

def load_rixs(scan_number):

    ccd1, ccd2, ccd3 = load_ccds(scan_number)
    ccd1 = x_corr(ccd2, ccd1)
    ccd3 = x_corr(ccd2, ccd3)
    xdata = np.arange(len(ccd2))
    ydata = ccd1 + ccd2 + ccd3

    return xdata, ydata
```

```python
if __name__ == "__main__":
    project_path = "X:/RIXS/Asmara/"
    base_atom = "O"
    energy_dispersion = 0.00457  # eV/subpixel

```