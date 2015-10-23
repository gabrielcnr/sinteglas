from setuptools import setup, find_packages

def get_version():
    import sinteglas
    return sinteglas.version


entry_points = {
    'console_scripts': [
        'sinteglas = sinteglas.main:main',
    ],
}


setup(
    name='sinteglas',
    version=get_version(),
    packages=find_packages(),
    entry_points=entry_points,
)