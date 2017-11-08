from setuptools import setup

setup(
    name="bookscrapper",
    version="0.1",
    packages=['bookscrapper'],
    install_requires=['requests', 'bs4', 'lxml'],
    entry_points={
        'console_scripts': ['scrapbook = bookscrapper.scrapbook:main']
    },
    python_requires='>=3.2',
)
