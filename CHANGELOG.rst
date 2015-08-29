.. :changelog:

Change Log
----------

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning`_. The change log is
formatted as suggested by `Keep a CHANGELOG`_.

`0.2`_
~~~~~~~~~~~~~

Added

* Support for directories
* Option 'keep_top_dir' to keep the top level directory (instead of only
  copying its content). Possible values are: True, False (default)
* Option 'on_duplicate' to specify what to do when duplicate files or
  directories are encountered. Possible values are: 'exception' (default),
  'ignore', 'overwrite'

`0.1`_
~~~~~~~

Added

* Specify one or multiple files to be copied by decorating the test
  function


.. _`0.2`: https://github.com/omarkohl/pytest-datafiles/compare/0.1...0.2
.. _`0.1`: https://github.com/omarkohl/pytest-datafiles/compare/3c31b2c...0.1


.. _`Semantic Versioning`: http://semver.org/
.. _`Keep a CHANGELOG`: http://keepachangelog.com/
