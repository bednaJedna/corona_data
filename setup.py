from setuptools import setup, find_packages


setup(
    name="coronaMap",
    packages=find_packages(),
    install_requires=["pandas", "requests", "dash", "python-dateutil"],
)
