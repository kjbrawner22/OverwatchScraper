from setuptools import setup

setup(
	name='ow_scraper',
	version='0.1',
	description='Playoverwatch site scraper',
	author="Kenny Brawner",
	author_email="kjbrawner@crimson.ua.edu",
	py_modules=['ow_scraper'],
	install_requires=[
		'beautifulsoup4',
	]
)