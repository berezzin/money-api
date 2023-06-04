What is it Money API?
It's backend service for helping you transaction accounting. There represented different microservices, such as: 
* Money application
* Redis cache service
* Postgres database
* Celery background tasks
* Flower tasks dashboard

If you are impressed and want to deploy this wonderfull web application on your server you just need 3 steps:
1. Clone this repo 
2. Create in the root folder of project .env-prod file with required environment variables as in example bellow
![image](https://github.com/berezzin/money-api/assets/101830798/c2e122ed-2d3e-4aba-b101-ec38ba9e76ee)
4. Run `docker compose -f .\docker-compose-prod.yaml up` command inside the root folder of repository.
