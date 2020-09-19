from setuptools import setup
import setuptools

setup(name='gym_connect',
      version='0.0.1',
      install_requires=[
            'gym',
            'pygame', # For ubuntu 20.04 install pygame==2.0.0.dev6
            'numpy'],#And any other dependencies required
      description='Connect4 and Connect2 games with different options',
      author='frknayk',
      author_email='furkanayik@outlook.com',
      packages=setuptools.find_packages(),
      python_requires='>=3.5'
      )
