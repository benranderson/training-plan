# Training Plan
> Create a bespoke running training plan

Web application for creating a bespoke running training plan for your event and ability level.

Hosted at <https://training-plan-br.herokuapp.com>.

[![Build Status][travis-image]][travis-url]
[![Coverage Status][coveralls-image]][coveralls-url]

## Features

Covers 5k, 10k, half marathon and full marathon events and beginner, intermediate and advanced ability levels.

## Development setup (UNIX)

First clone the repository to desired folder location:

```sh
$ git clone https://github.com/benranderson/training-plan.git
```

Navigate into app directory:

```sh
$ cd training-plan
```

Install dependencies:

```sh
$ pip install -r requirements.txt
```

Run the server:

```sh
$ python manage.py runserver
```

To run unit tests, first install testing dependencies:

```sh
$ pip install -r requirements/dev.txt
```

Then run tests:

```sh
$ python manage.py test
```

## Release History

* 0.0.1
    * Work in progress

## Meta

Ben Randerson – ben.m.randerson@gmail.com

[https://github.com/benranderson](https://github.com/benranderson)

<!-- Markdown link & img dfn's -->
[travis-image]: https://www.travis-ci.org/benranderson/training-plan.svg?branch=master
[travis-url]: https://www.travis-ci.org/benranderson/training-plan
[coveralls-image]:
https://coveralls.io/repos/github/benranderson/training-plan/badge.svg?branch=master
[coveralls-url]:
https://coveralls.io/github/benranderson/training-plan?branch=master
