from setuptools import setup

setup(
    name='api',
    packages=['api', 'models', 'data', 'user', 'jwt_token', 'emails'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
