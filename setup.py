from distutils.core import setup

setup(
    name='css2py',
    #author='none',
    #author_email='none',
    url= 'https://github.com/pinocchio964/css2py',
    description= 'Experimental python css-based engine to styling custom xml files.',
    version='1.0',
    #data_files=[('/usr/local/sbin', ['sire'])],
    packages=[
        'css2py',
    ],
    package_dir={
        'sire'              : 'src',
    },
    #package_data={
    #    'sire.web' : ['css/*.css', 'image/*.*', 'js/*.js', '*.html']
    #}
)
