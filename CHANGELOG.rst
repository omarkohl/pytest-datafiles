.. :changelog:

Change Log
----------

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning`_. The change log is
formatted as suggested by `Keep a CHANGELOG`_.

`Unreleased`_
~~~~~~~~~~~~~

Added
Changed
Deprecated
Removed
Fixed
Security

`3.0`_
~~~~~~

Changed

* BREAKING CHANGE: Using `pathlib.Path` instead of `py.path` (`#7`_)
* BREAKING CHANGE: Removed support for Python 2.7 and Python 3 <= 3.6

`2.0.1`_
~~~~~~~~

Fixed

* Register custom marker 'datafiles' to avoid PytestUnknownMarkWarning
  (`#18`_)

`2.0`_
~~~~~~

Added

* Explicit support for Python 3.6 (no changes were necessary)

Removed

* BREAKING CHANGE: Python 2.6 is no longer supported (because we rely on pytest
  >= 3.6)

Fixed

* Use the new pytest mark API to fix MarkInfo warnings (`#2`_)
* BREAKING CHANGE: Symlinks are now copied as links instead of copying the
  target they point to (`#1`_)

`1.0`_
~~~~~~

Changed

* Bump version to 1.0 to signal that the plugin is stable
* Minor refactorization without repercussions for users
* Only use regular 'paths' (str) instead of py.path objects in documentation
  examples because they were confusing to some people (unfamiliar with py.path)

`0.2`_
~~~~~~

Added

* Support for directories
* Option 'keep_top_dir' to keep the top level directory (instead of only
  copying its content). Possible values are: True, False (default)
* Option 'on_duplicate' to specify what to do when duplicate files or
  directories are encountered. Possible values are: 'exception' (default),
  'ignore', 'overwrite'

`0.1`_
~~~~~~

Added

* Specify one or multiple files to be copied by decorating the test
  function


.. _`Unreleased`: https://github.com/omarkohl/pytest-datafiles/compare/3.0...master
.. _`3.0`: https://github.com/omarkohl/pytest-datafiles/compare/2.0.1...3.0
.. _`2.0.1`: https://github.com/omarkohl/pytest-datafiles/compare/2.0...2.0.1
.. _`2.0`: https://github.com/omarkohl/pytest-datafiles/compare/1.0...2.0
.. _`1.0`: https://github.com/omarkohl/pytest-datafiles/compare/0.2...1.0
.. _`0.2`: https://github.com/omarkohl/pytest-datafiles/compare/0.1...0.2
.. _`0.1`: https://github.com/omarkohl/pytest-datafiles/compare/3c31b2c...0.1


.. _`#1`: https://github.com/omarkohl/pytest-datafiles/issues/1
.. _`#2`: https://github.com/omarkohl/pytest-datafiles/issues/2
.. _`#7`: https://github.com/omarkohl/pytest-datafiles/issues/7
.. _`#18`: https://github.com/omarkohl/pytest-datafiles/issues/18


.. _`Semantic Versioning`: http://semver.org/
.. _`Keep a CHANGELOG`: http://keepachangelog.com/
