"""
CADENCE — toolchain smoke test.

Repository: https://github.com/muhammedfahim438-ctrl/CADENCE
"""


def test_toolchain_works() -> None:
    import pandas as pd
    import numpy as np

    assert int(pd.__version__.split(".")[0]) >= 2
    assert np.array([1, 2, 3]).sum() == 6