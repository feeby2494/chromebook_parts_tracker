from setuptools import setup

setup(
    name='api',
    packages=['api', 'models', 'data', 'admin', 'token'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
