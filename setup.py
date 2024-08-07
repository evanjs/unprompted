# Strictly for use outside of the WebUI. This file will allow you to install Unprompted via pip. Example:
# pip install unprompted@git+https://github.com/ThereforeGames/unprompted

from setuptools import setup

setup(
    name='Unprompted',
    version='11.2.0',
    package_dir={'unprompted': '.'},
    packages=['unprompted.lib_unprompted', 'unprompted.shortcodes', 'unprompted.shortcodes.basic', 'unprompted.shortcodes.stable_diffusion', 'unprompted.templates', 'unprompted.docs'],
    package_data={
        'unprompted.lib_unprompted': ['*.json'],
        'unprompted.templates': ['common/*.txt'],
        'unprompted.docs': ['*.md']
    },
    include_package_data=True,
)
