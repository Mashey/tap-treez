from setuptools import setup, find_packages

setup(
    name="tap-treez",
    version="0.1.0",
    description="Singer.io tap for extracting data from the Treez API",
    author="Ryan Allen",
    url="https://code.treez.io/",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_treez"],
    install_requires=[
        "singer-python==5.9.0",
        "requests"
    ],
    entry_points="""
    [console_scripts]
    tap-treez=tap_treez:main
    """,
    packages=["tap_treez"],
    package_data={
        "tap_treez": ["schemas/*.json"]
    },
    include_package_data=True,
)
