from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='crdtpy',
      version='0.1',
      description='Python package for CRDT datatype database',
      long_description=readme(),
      url='https://github.com/kishore-narendran/crdt-py.git',
      author='Kishore Narendran, Sai Teja Ranuva',
      author_email='sranuva@uci.edu',
      keywords='Distributed Systems CRDT Strong Eventual Consistency Database',
      license='MIT',
      packages=find_packages(),
      setup_requires=['nose>=3.5'],
      zip_safe=False)
