# Build
The steps to build/execute this project are the following:
1. Download the repository
2. Create an environment which accepts a requirements.txt (Conda, virtualenv)
3. Install all the packages by running  `pip install -r devops/requirements.txt`
4. Install Docker and  docker-compose
5. Run the command: `docker-compose -f devops/docker-compose.yml up`
6. Setup the ENV variables DB_HOST, DB_USER, DB_PWD, DB_PORT (default: localhost, postgres, postgres, 5432)
7. Run any of the spiders using python main.py --spider_name={spider_name} 
(name is one of the files inside src/spiders) such as "animenews"