from setuptools import setup

setup(
    name="bookscrapper",
    version="1.0",
    packages=['bookscrapper'],
    install_requires=['requests', 'bs4', 'lxml'],
    entry_points={
        'console_scripts': ['scrapbook = bookscrapper.scrapbook:main']
    },
    python_requires='>=3.2',
    zip_safe=True,
)
