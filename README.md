# AMAMB [![Build Status](https://travis-ci.org/washingt0/amamb-ifce.svg)](https://travis-ci.org/washingt0/amamb-ifce)

Open Source lightweight Web App that dynamically generates basic mathematical problems.
It's intended to provide an intuitive practical experience to students in basic education.

## Prerequisites

- [Python](https://www.python.org/) >= 2.7 (2.7 recommended)
- [pip](https://pip.pypa.io/en/stable/) (already bundled with Python >= 2.7.9)
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/index.html) (Recommended to avoid dependecies conflicts)

## Installing

Download the code

    $ git clone https://github.com/washingt0/amamb-ifce.git

Create the virtual environment

    $ cd amamb-ifce
    $ virtualenv env

Install dependencies

    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ deactivate

## Running

Every time before running the application, you have to activate the virtual environment:

    $ source env/bin/activate

Then run the application:

    $ python app.py

You should see something like:

    * Restarting with stat
    * Debugger is active!
    * Debugger pin code: 161-475-591
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Now you should be able to access `http://localhost:5000/` in your web browser.
