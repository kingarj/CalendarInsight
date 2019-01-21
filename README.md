# Insight
[![Build Status](https://travis-ci.com/kingarj/CalendarInsight.svg?branch=master)](https://travis-ci.com/kingarj/CalendarInsight)

A Flask application using the Google Calendar API to give users an insight as to how they are spending their time.
Features include event keyword search and graphical representations of time spent in different activities.

## Getting Started

Use the requirements.txt file to pip install the dependencies.
Create a set of credentials using [Google Developer API console](https://console.developers.google.com/apis/credentials)
Download the `credentials.json` file to the root of the project.

### Prerequisites

* Python 3
* An IDE that supports development of a Flask application e.g. PyCharm

### Environment variables

You will need to set FLASK_APP, FLASK_ENV and SECRET KEY; which are pre-requisite variables of Flask.
For development you will need to set the following:
* OAUTHLIB_INSECURE_TRANSPORT=1
* REDIRECT_URI=http://127.0.0.1:5000/authenticate
* ROOT_URL=http://127.0.0.1:5000
* OAUTH_CREDENTIALS={name of your credentials.json file}

## Running the tests

To run the tests, use `python -m pytest`. To collect coverage, add a `--cov=app` flag to the command.

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Google Calendar API](https://developers.google.com/calendar/)

## Authors

* **Alice King** - [kingarj](https://github.com/kingarj)
