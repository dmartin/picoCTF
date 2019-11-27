"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


# Always prefer setuptools over distutils
from setuptools import find_packages, setup

setup(
    name="pico-api",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="2.0.0",
    description="picoCTF API",
    # The project's main homepage.
    url="https://github.com/picoCTF/picoCTF",
    # Author details
    author="picoCTF team",
    author_email="opensource@picoctf.com",
    # Choose your license
    license="",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
    ],
    # What does your project relate to?
    keywords="ctf hacksports",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "bs4==0.0.1",
        "cchardet==2.1.4",
        "eventlet==0.25.1",
        "Flask==1.1.1",
        "Flask-Bcrypt==0.7.1",
        "Flask-Mail==0.9.1",
        "flask-restplus==0.13.0",
        "gunicorn==19.9.0",
        "marshmallow==3.0.1",
        "py==1.8.0",
        "pymongo==3.9.0",
        "spur==0.3.21",
        "voluptuous==0.11.7",
        "walrus==0.7.1",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "locustio",
            "pydocstyle",
            "pytest",
            "pytest-cov",
            "pytest-mongo",
            "pytest-redis",
        ]
    },
)
