from setuptools import find_packages,setup
from typing import List

def get_requirements(file:str) -> List[str]:
    '''
    This is for fetching the list of libraries that will be
    used in this project
    '''
    requirements = []
    with open(file) as file_pack:
        requirements = file_pack.readlines()
        [requirement.replace("\n", " ") for requirement in requirements]
        
        if "-e ." in requirements:
            requirements.remove("-e .")
    
    return requirements


setup(
    name = "DS_practice_proj",
    version = '0.0.1',
    author = "Arthakorn",
    author_email = "arthakornpetch@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements("requirements.txt")
)