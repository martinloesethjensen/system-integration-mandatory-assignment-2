# system-integration-mandatory-assignment-2

Bank System
=====

Run services
-----------

Run bank services at once with all the sub-services
* docker-compose up --build

Access services individually
* Bank API --> http://localhost:8080/api/{controller}{endpoint}
* DB --> localhost:1433 - ID:SA PW:Password1!
* Interest Rate Function --> http://localhost:8082/api/Interest_rate_function
* Loan Algorythm Function--> http://localhost:8083/api/Loan_Algorythm_Function