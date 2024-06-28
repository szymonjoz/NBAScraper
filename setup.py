from setuptools import setup

setup(
    name='NBAScraper',
    version='1.0',
    packages=["NBAScraper"],
    package_data={
        'NBAScrape': ['preschedule.csv'],
    }
    install_requires=[
        "selenium>=4",
        "pandas>=2",
        "lxml>=4"
    ],
    author='Szymon Jóźwiak',
    author_email='szymon.joz.kontakt@gmail.com',
    description='Webscraper for nba.com/stats data',
    long_description_content_type='text/markdown',
    url='https://github.com/szymonjoz/NBAScraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
