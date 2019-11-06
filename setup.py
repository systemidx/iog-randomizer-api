import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iog-randomizer-api',
    version='2.5.1',
    description='The Illusion of Gaia Randomizer API',
    author='bryon_w',
    packages=setuptools.find_packages(),
    install_requires=['flask', 'flask_expects_json','flask_cors', 'iog_randomizer'],
    python_requires='>=3.7'
)
