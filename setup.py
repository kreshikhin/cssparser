from distutils.core import setup, Extension
from distutils.command.build import build
import subprocess
import os

class pre_build(build):
    def run(self):
        try:
            cwd = os.getcwd()
            os.chdir("./src/cssparser/")
            subprocess.call(["flex", "-d", "css.l"])
            subprocess.call(["yacc", "-d", "css.y"])
            os.chdir(cwd)
        except:
            print("Please install flex and yacc on your system before build the css2py package. ")
            quit()
        super().run()


cssparser = Extension(
    'css2py.cssparser',
    sources = ['src/cssparser/css.c', 'src/cssparser/y.tab.c', 'src/cssparser/lex.yy.c'])

setup(
    name='css2py',
    #author='none',
    #author_email='none',
    url= 'https://github.com/pinocchio964/css2py',
    description= 'Experimental python css-based engine to styling custom xml files.',
    version='1.0',
    packages=[
        'css2py',
    ],
    package_dir={
        'css2py'              : 'src',
    },
    ext_modules = [cssparser],
    cmdclass={"build" : pre_build}
)
