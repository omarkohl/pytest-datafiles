# simple pytest wrapper so we can execute it using "coverage run"
import sys

import pytest

sys.exit(pytest.main())
