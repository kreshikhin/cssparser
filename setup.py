from distutils.core import setup, Extension
from distutils.command.build import build
import subprocess
import os

class pre_build(build):
    def run(self):
        try:
            cwd = os.getcwd()
            os.chdir("./src/")
            print("================ FLEX =====================")
            subprocess.call(["flex", "-d", "css.l"])
            print("\n")
            print("================ YACC =====================")
            subprocess.call(["yacc", "-d", "css.y"])
            print("\n")
            os.chdir(cwd)
        except:
            print("Please install flex and yacc on your system before build the cssparser package. ")
            quit()
        super().run()


cssparser = Extension(
    'cssparser',
    sources = ['src/cssparser.c', 'src/y.tab.c', 'src/lex.yy.c'])

setup(
    name='css2py',
    author='pinocchio964',
    author_email='pelou85@gmail.com',
    url= 'https://github.com/pinocchio964/css2py',
    description= 'Experimental python CSS parser.',
    version='1.0',
    packages=[
        'cssparser',
    ],
    package_dir={
        'cssparser'              : 'src',
    },
    ext_modules = [cssparser],
    cmdclass={"build" : pre_build}
)
