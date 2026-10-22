from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'g10_prii3_turtlesim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryuu4',
    maintainer_email='tu_email@ejemplo.com',
    description='Control de turtlesim para el grupo 10',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_controller = g10_prii3_turtlesim.turtle_controller:main',
        ],
    },
)
