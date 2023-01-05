import numpy as np


def fileListGenerator(numberString):
    """Function to generate list of data files.

    Args:

        - numberString (str): List if numbers separated with comma and dashes for sequences.

        - folder (str): Folder of wanted data files.

    returns:

        - list of strings: List containing each number provided.

    Example:
        >>> numberString = '201-205,207-208,210,212'
        >>> files = fileListGenerator(numberString)
        [201,202,203,204,205,207,208,210,212]
    """

    splits = numberString.split(",")
    dataFiles = []

    for sp in splits:
        isRange = sp.find("-") != -1

        if isRange:
            spSplits = sp.split("-")
            if len(spSplits) > 2:
                raise AttributeError(
                    'Sequence "{}" not understood - too many dashes.'.format(sp)
                )
            startNumber = int(spSplits[0])
            endNumber = int(spSplits[1])
            if startNumber > endNumber:
                numbers = np.arange(startNumber, endNumber - 1, -1)
            else:
                numbers = np.arange(startNumber, endNumber + 1)
        else:
            numbers = [int(sp)]

        dataFiles.append([x for x in numbers])
    return list(np.concatenate(dataFiles))
