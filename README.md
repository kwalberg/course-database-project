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

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.



## Setup
Starting the server requires installing pip3, Python 3, Django 2, and a virtual environment.

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

The front page of Classy should be visible.

### Static Resources

In development, static assets are hosted at '<base_url>/static/' + namespacing appname + path to the asset within the 'myapp/static/myapp' directory. In your templates, include {% load staticfiles %} at the top of the template and reference static assets like,

    <img src="{% static 'appname/img/myimage.png' %}" alt="myimage">

proj uses the standard `django.contrib.staticfiles` app so in development, when the DEBUG setting is true, static assets are served automatically with runserver.


### Deploying Static Resources

In staging and production environments, using a web process to serve static assets is not appropriate. proj uses `django-storages` adapters to upload collected static assets to Amazon S3 and to replace static template tags correctly.

First, create [S3 buckets](https://console.aws.amazon.com/s3) proj-static-stag and proj-static (set in proj/settings/staging.py and proj/settings/production.py) for static assets. Then create two [IAM](https://console.aws.amazon.com/iam/home) users proj_stag and proj with the Full S3 Access permission policy.

Be sure the APP_ENV, SECRET_KEY, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY environment variables are set in your environment.

Upload static files,

    python manage.py collectstatic  # when APP_ENV is staging or production

Then, in staging and production, the static assets uploaded to the staging and production buckets, respectively, will be referenced in your templates.

*Note: If a STATIC_ROOT directory was created in your project directory, your APP_ENV is set to development. Delete the STATIC_ROOT directory.*
