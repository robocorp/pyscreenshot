import os.path

from setuptools import setup

if os.environ.get("distutils_issue8876_workaround_enabled", False):
    # sdist_hack: Remove reference to os.link to disable using hardlinks when
    #             building setup.py's sdist target.  This is done because
    #             VirtualBox VMs shared filesystems don't support hardlinks.
    del os.link

NAME = "rpaframework-screenshot"
URL = "https://github.com/robocorp/rpaframework-screenshot"
DESCRIPTION = "rpaframework screenshot"
PACKAGES = [
    "pyscreenshot",
    "pyscreenshot.cli",
    "pyscreenshot.plugins",
    "pyscreenshot.examples",
]

# get __version__
__version__ = None
exec(open(os.path.join("pyscreenshot", "about.py")).read())
VERSION = __version__

# extra = {}
# if sys.version_info >= (3,):
#     extra['use_2to3'] = True
#     extra['use_2to3_exclude_fixers'] = ['lib2to3.fixes.fix_import']

classifiers = [
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

install_requires = [
    "EasyProcess",
    "mss ; python_version > '3.4'",
    "jeepney ; python_version > '3.4' and platform_system == 'Linux'",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst", "r").read(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=classifiers,
    keywords="rpaframework-screenshot",
    author="ponty",
    # author_email='',
    url=URL,
    license="BSD",
    packages=PACKAGES,
    #     include_package_data=True,
    #     test_suite='nose.collector',
    #     zip_safe=False,
    install_requires=install_requires,
    # **extra
)
