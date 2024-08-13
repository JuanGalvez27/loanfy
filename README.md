# Loanfy

Awesome API to provide information and management of loans.

## Requirements Links

[Docker](https://docs.docker.com/engine/install/)

## Basic Commands

In order to launch the project locally enter the project repository and execute

``` plain
docker compose up -d --build
```

### Setting Up Your Users

- To create a **superuser account**, use this command:

      docker exec -it loanfy-loanfy-1 python3 manage.py createsuperuser

#### Running tests

    $ docker exec -it loanfy-loanfy-1 coverage run manage.py test

### Test coverage

To run the tests, check your test coverage:

    $ docker exec -it loanfy-loanfy-1 coverage report
    
## API Docs 

The app's documentation was created with Swagger and can be accessed as follows:

- Visit http://localhost:8000/