# Similarity Check API using Spacy NLP Models

## Description
API for finding similarity between two sentences or strings. Built with Python, Flask, MongoDB and Spacy
NLP Models.

- User can sign up for using API by sending json object of username and password at /register
```
{
    "username": "user",
    "password": "pass"
}
```
- User can check similarity of two sentences by sending post request at /detect. This action deducts one token
```
{
    "username": "user",
    "password": "pass",
    "text1": "hello my first sentence",
    "text2": "hello, are they similar ?
}
```
Response
```
{
    "status": 200
    "similarity": 0.651514
}
```
- Admin can refill user tokens by hitting /refill endpoint
```
{
    "username": "user"
    "admin_pw": "adminpass"
    "refill": 10
}
```
- status 301 means out of tokens
- status 302 means invalid username or password

## How to run
* Clone the repo
* $ cd text-similarity
* $ docker-compose build
* $ docker-compose up
* Open new terminal/cmd
* Find you docker machine IP by typing
* $ docker-machine ip
* Open your browser and type : http://your-docker-machine-ip:5000/
* if helloworld appears then its working fine
* Test API using POSTMAN