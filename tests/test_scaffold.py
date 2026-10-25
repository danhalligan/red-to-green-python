from importlib import resources

import exercises
import exercises._shared


def test_package_imports():
    assert exercises.__doc__


def test_shared_data_is_discoverable():
    assert resources.files(exercises._shared).joinpath("data").is_dir()
