from setuptools import setup


DEPENDENCIES = [
    'py',
    'pytest',
    ]

DESCRIPTION = ("py.test plugin to create a 'tmpdir' containing predefined "
	       "files/directories.")
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pytest-datafiles',
    version='0.1.dev0',
    py_modules=['pytest_datafiles'],
    url='https://github.com/omarkohl/pytest-datafiles',
    license='MIT',
    install_requires=DEPENDENCIES,
    author='Omar Kohl',
    author_email='omarkohl@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    entry_points={
        'pytest11': ['pytest_datafiles = pytest_datafiles'],
	},
    keywords='pytest datafiles tmpdir',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Testing',
	]
    )
