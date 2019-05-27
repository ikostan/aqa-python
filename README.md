# AQA Python course


## Allure reports

allure reports folder: 

`tests/reports/allure-results`

generate and show allure report:

`allure serve tests/reports/allure-results`


## Run tests

### Run all tests 
`$ pytest --alluredir=tests/reports/allure-results`

### Run "unite" tests
- fibonacci
- XML to JSON file processor
 
`$ pytest -m unit --alluredir=tests/reports/allure-results`

### Run UI tests
 
`$ pytest -m ui --alluredir=tests/reports/allure-results`

### Run REST tests
 
`$ pytest -m rest --alluredir=tests/reports/allure-results`
