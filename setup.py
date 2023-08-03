from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hdfc_integration_client/__init__.py
from hdfc_integration_client import __version__ as version

setup(
	name="hdfc_integration_client",
	version=version,
	description="HDFC Integration Client",
	author="Aerele Technologies Private Limited",
	author_email="hello@aerele.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
