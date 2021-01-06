# system-integration-mandatory-assignment-2

## Bank Service

### Run services

Run bank services at once with all the sub-services
* docker-compose up --build

Access services individually
* Bank API --> http://localhost:8080/api/{controller}{endpoint}
* DB --> localhost:1433 - ID:SA PW:Password1!
* Interest Rate Function --> http://localhost:8082/api/Interest_rate_function
* Loan Algorythm Function--> http://localhost:8083/api/Loan_Algorythm_Function

### Bank Service definition
-----------

After starting the service find API docs on **{host}:{port}/swagger/index.html**

## Skat Service

Documentation on how to run the service locally is available in the [README.md](Skat/README.md)

### Endpoint Definitions

API file: [insomnia.json](insomnia.json)
