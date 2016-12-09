"""
A binary wire protocol/serialization library for python3.
"""

from setuptools import find_packages, setup

setup(
    name='bpickle',
    version='0.0.1',
    license='GPLv3',
    author='Chris Glass',
    author_email='chris.glass@canonical.com',
    description='A binary serialization library for python3',
    long_description=__doc__,
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    #install_requires=dependencies,
    #dependency_links=dependency_links,
)
