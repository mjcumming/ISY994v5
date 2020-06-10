import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='ISY994v5',
    version='0.8.9',
    description='ISY99 Controller Rest and Websocket client v5 firmware',
    author='Michael Cumming',
    author_email='mike@4831.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mjcumming/ISY994v5',
    keywords=['INSTEON', 'ISY994', 'ISY', 'Universal Devices'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp',
    ]
)
