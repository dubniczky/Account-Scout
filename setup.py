from setuptools import setup, find_packages

setup(
    name = "accscout",
    version = "1.0",
    author = "Richard Antal Nagy",
    license = "MIT",
    keywords = [ "accscout", "account", "security", "hacking", "OSINT", "crawler" ],
    url = "https://gitlab.com/richardnagy/security/accscout",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
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
)