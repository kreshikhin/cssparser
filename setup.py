from distutils.core import setup, Extension
from distutils.command.install_data import install_data

class post_install(install_data):
    def run(self):
        # Call parent 
        # install_data.run(self)
        # Execute commands
        print("Running")


cssparser = Extension('css', sources = ['src/cssparser/css.c'])

setup(
    name='css2py',
    #author='none',
    #author_email='none',
    url= 'https://github.com/pinocchio964/css2py',
    description= 'Experimental python css-based engine to styling custom xml files.',
    version='1.0',
    packages=[
        'css2py',
        'css2py.cssparser',
    ],
    package_dir={
        'css2py'              : 'src',
        'css2py.cssparser'    : 'src/cssparser'
    },
    ext_modules = [cssparser],
    cmdclass={"install_data": post_install}
)
