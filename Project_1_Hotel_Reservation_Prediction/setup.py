from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines() # read lines from requirements.txt, store in list
    
    setup (
        name= "MLOPS-PROJECT-1-HOTEL-RESERVATION-PREDICTION",
        version= "0.1",
        author= "Sena Nur Bilgin",
        author_email= "senanrbilgin@gmail.com",
        description= "A project to predict hotel reservations using machine learning.",
        packages= find_packages(), # automatically find packages in the directory
        install_requires= requirements, # use the requirements list defined above
    )
    
    