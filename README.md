# Classy


Classy is a Django-hosted web app that scrapes course information, and builds a easy-to-read course catalog with sorting, commenting, rating, and tagging features.

The main purpose of this software project is to learn about software development and work as a team to produce a product for our computer science course, COMP 225 Software Design and Development, taught by Professor Elizabeth Jensen.

# Tech Stack
- Django 2.0
- Python 3
- Bootstrap 4
- JQuery
- Javascript
- MySQL
- Amazon Web Services for Deploy

## Setup
Starting the server requires installing pip3, Python 3, Django 2, and a virtual environment.

Once you have these requirements installed, clone or download the repository
and navigate to the download location from the command line.

Create a virtual environment in which to install Python pip packages. Virtual environment activation with [virtualenv](https://pypi.python.org/pypi/virtualenv),

    virtualenv venv          # create virtualenv venv
    source venv/bin/activate # activate

or with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/),

    mkvirtualenv myproj       # create and activate environment
    workon myproj             # reactivate existing environment

Install development dependencies,

    pip install -r requirements.txt

Run the web application locally,

    python3 manage.py runserver # 127.0.0.1:8000

Once you have entered the command to run the server, go to 127.0.0.1:8000 in your
 favorite web browser. The front page of Classy should be visible.

