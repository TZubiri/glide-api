# glide-api

Technical challenge for position at Glide

# Overview

The objective of the task was to build a unified api that collected data from a file and an external api. 

The api was designed to demonstrate the level of quality I would like to work with, as well to showcase my skills and areas of competence.

# Tech stack

The api server was built using the following technologies:
*  Python 3.8: for requirement's logic and providing a base dependency for most libraries used.
*  [Fla](https://palletsprojects.com/p/flask/)[sk](https://flask.palletsprojects.com/en/1.1.x/foreword/#what-does-micro-mean): For routing incoming http requests and the general architectural benefits of an opinionated framework.
*  [Requests](https://requests.kennethreitz.org/en/master/user/intro/#philosophy): For making outgoing connections to the external api and testing our own api. 
*  [Nginx](https://translate.google.com/translate?hl=&sl=ru&tl=en&u=https%3A%2F%2Fru.m.wikipedia.org%2Fwiki%2FNginx)-[Gunicorn](https://www.python.org/dev/peps/pep-0333/): For handling multiple http connections and future https support.
*  [Docker](https://blog.jessfraz.com/post/docker-containers-on-the-desktop/): For packaging the application along with its dependencies and providing unified behaviour between dev machines and deployment servers.
*  [Docker-compose](https://docs.docker.com/compose/): For providing a clean ui for running the app and test harness.
*  [G](https://en.wikipedia.org/wiki/Git#History)[i](http://think-like-a-git.net/)[t](https://git-man-page-generator.lokaltog.net/)t: For branching, reverts, development history and code delivery.
*  [Debian](https://www.gnu.org/licenses/copyleft.en.html): For container base and usage bash scripts

# How to run

The easiest way to run the server and test harness is to
* [install Docker](https://docs.docker.com/install/).
* [install Docker-compose](https://docs.docker.com/compose/install/)
* run docker-compse up
* test the api at http://localhost/employees

The second easiest way is to:
* install [python 3.8](https://www.python.org/downloads/release/python-380/)
* pip install Flask
* pip install requests
* python3 app.py
* test the api at http://localhost:5000/employees

#Post-mortem notes:

* Perhaps a json database like MongoDB or ArangoDB could have been used to avoid the development of the Expand engine. This would have also provided some caching mechanisms.
* Perhaps parametrizing the endpoint string in routes could have avoided a lot of code repetition at the cost of stringifying the business objects (employees, offices).
* I went for caching as a way to reduce external api hits,but queries with a medium sized limit and deeply nested expansions might cause a lot of single api queries. The most helpful method here would be to perform api queries in chunks within the expand function. However this has a lot of architectural complexity since this is the most complex function. It might be optimized in place by parallelizing the loop and waiting until n requests are ready to be sent before actually sending them.
