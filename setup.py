"""
thedenbot

"""

from setuptools import setup, find_packages

def get_requirements():
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    return required


setup(
    name='thedenbot',
    version='0.1.0',
    description='a telegram bot',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=get_requirements(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'thedenbot=thedenbot.bot:main',
        ],
    },
)
