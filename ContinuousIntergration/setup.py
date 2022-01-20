from distutils.core import setup

from setuptools import find_packages

try:
    from RoutingServer.version import __version__
except:
    exec(open("RoutingServer/version.py").read())

setup(
    name="RoutingServer",
    version=__version__,
    packages=find_packages(),
    package_data={p: ["*"] for p in find_packages()},
    url="",
    license="",
    install_requires=["fastapi", "pydantic", "uvicorn", "click", "numpy", "pyzmq"],
    python_requires=">=3.8.0",
    author="Tom.McLean",
    author_email="tom.mclean@bartechnologies.uk",
    description="Routing Server",
)
