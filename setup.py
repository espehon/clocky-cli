from setuptools import setup
exec(open('clocky_pkg/__init__.py').read())
setup(
    name = 'clocky',
    version = __version__,
    package = ['clocky_pkg'],
    entry_points = {'console_scripts': ['clocky = clocky_pkg.__main__:main']
    })
