from importlib import resources

import pyproblems
import pyproblems.datasets


def test_package_imports():
    assert pyproblems.__doc__


def test_dataset_package_is_discoverable():
    assert resources.files(pyproblems.datasets).is_dir()
