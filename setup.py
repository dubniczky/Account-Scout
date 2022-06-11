from setuptools import setup, find_packages
from os import getenv

version = getenv('CI_COMMIT_TAG', 'v0.1')[1:]

setup(
    name = "accscout",
    version = version,
    author = "Richard Antal Nagy",
    author_email="nagy.richard.antal@gmail.com",
    description="Search for certain user accounts on popular websites on the internet",
    license = "MIT",
    keywords = [ "accscout", "account", "security", "hacking", "OSINT", "crawler" ],
    url = "https://gitlab.com/richardnagy/security/accscout",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml',
        'requests',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'accscout = accscout.__main__:main'
        ]
    },
    python_requires='>=3.8',
)