from setuptools import find_packages, setup

setup(
    name='eDisGo',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/openego/eDisGo',
    license='GNU Affero General Public License v3.0',
    author='gplssm, nesnoj',
    author_email='',
    description='A python package for distribution grid analysis and optimization',
    install_requires = [
        'dingo>=0.1.0',
        'networkx >=1.11',
        'shapely >= 1.5.12, <= 1.5.12',
        'pandas >=0.19.2, <=0.20.1'
    ]
)
