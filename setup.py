from setuptools import setup, find_packages
import versioneer


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='independent-jobs',
    author='Heiko Strathmann',
    author_email='heiko.strathmann@gmail.com',
    url="https://github.com/karlnapf/independent-jobs/",
    packages=find_packages(),
    description="Python framework for independent computation with backends for batch clusters",
    install_requires=requirements,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,  # so  nosetests --exe independent_jobs  will work
)
