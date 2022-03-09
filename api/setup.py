from setuptools import setup

setup(
    name='api',
    packages=['api', 'models', 'data', 'user', 'token', 'emails'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
