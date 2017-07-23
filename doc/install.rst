==========================
Installing PYBOSSA by hand
==========================

PYBOSSA is a python web application built using the Flask micro-framework.

You need this guide if you want to

 * Create a PYBOSSA for development or testing purposes
 * First step to create a production ready PYBOSSA. Second step for that is :doc:`nginx`.

Officially supported requirements:

  * Ubuntu 16.04 LTS
  * Python >= 2.7.6, <3.0
  * PostgreSQL >= 9.5
  * Redis >= 2.6
  * pip >= 6.1

It may also run with older software but we do not officially support it:

  * Ubuntu 14.04 LTS
  * Python >= 2.7.2, <3.0
  * PostgreSQL >= 9.3
  * Redis >= 2.6
  * pip >= 6.1

Setting things up
=================

Before proceeding to install PYBOSSA you will need to configure some other
applications and libraries in your system. In this page, you will get a step by
step guide about how to install all the required packages and libraries for
PYBOSSA using the latest `Ubuntu Server Long Term Support`_ version available at
the moment:

  * `Ubuntu 14.04 LTS`_

.. _`Ubuntu Server Long Term Support`: https://wiki.ubuntu.com/LTS
.. _`Ubuntu 14.04 LTS`: http://www.ubuntu.com/download/server

Installing git - a distributed version control system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PYBOSSA uses the git_ distributed version control system for handling the
PYBOSSA server source code as well as the template projects.

Git_ is a free and open source distributed version control system designed to
handle everything from small to very large projects with seepd and efficiency.

.. _git: http://git-scm.com/

.. _Git: http://git-scm.com/

In order to install the software, all you have to do is::

    sudo apt-get install git-core

Installing the PostgreSQL database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PostgreSQL_ is a powerful, open source object-relational database system.
It has more than 15 years of active development and a proven architecture that
has earned it a strong reputation for reliability, data integrity, and correctness.

PYBOSSA uses PostgreSQL_ as the main database for storing all the data, and you
the required steps for installing it are the following::

    sudo apt-get install postgresql postgresql-server-dev-all libpq-dev python-psycopg2

.. _PostgreSQL: http://www.postgresql.org/


Installing virtualenv (optional, but recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We recommend to install PYBOSSA using a `virtualenv`_ as it will create a an
isolated Python environment, helping you to manage different dependencies and
versions without having to deal with root permissions in your server machine.

virtualenv_ creates an environment that has its own installation directories,
that doesn't share libraries with other virtualenv environments (and
optionally doesn't access the globally installed libraries either).

You can install the software if you want at the system level if you have root
privileges, however this may lead to broken dependencies in the OS for all your
Python packages, so if possible, avoid this solution and use the virtualenv_
solution.

Installing virtualenv_ in the Ubuntu server could be done like this::

    sudo apt-get install python-virtualenv

After installing the software, now you will be able to create independent virtual
environments for the PYBOSSA installation as well as for the template
projects (see :doc:`user/tutorial`).

.. _virtualenv: http://pypi.python.org/pypi/virtualenv

Installing the PYBOSSA Python requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing the required libraries for PYBOSSA is a step that will need to use
some compilers and dev libraries in order to work. Thus, you will need to
install the following packages::

    sudo apt-get install python-dev build-essential libjpeg-dev libssl-dev libffi-dev dbus libdbus-1-dev libdbus-glib-1-dev

Then, you are ready to download the code and install the required libraries for
running PYBOSSA.

.. note::
    We recommend you to install the required libraries using a **virtual
    environment** with the command virtualenv (you can install the package
    python-virtualenv). This will allow to have all the libraries for PYBOSSA
    in one folder of your choice, so cleaning the installation would be as
    simple as deleting that folder without affecting your system.


If you decide to use a **virtualenv** then, follow these steps (lines starting
with **#** are comments)::

  # get the source code
  git clone --recursive https://github.com/Scifabric/pybossa
  # Access the source code folder
  cd pybossa
  virtualenv env
  # Activate the virtual environment
  source env/bin/activate
  # Upgrade pip to latest version
  pip install -U pip
  # Install the required libraries
  pip install -r requirements.txt


Otherwise you should be able to install the libraries in your system like
this::

  # get the source
  git clone --recursive https://github.com/Scifabric/pybossa
  # Access the source code folder
  cd pybossa
  # Upgrade pip to latest version
  pip install -U pip
  # Install the required libraries
  pip install -r requirements.txt

.. note::
    Vim_ editor is a very popular text editor in GNU/Linux systems, however it
    may be difficult for some people if you have never used it before. Thus, if
    you want to try another and much simpler editor for editing the
    configuration files you can use the `GNU Nano`_ editor.

Create a settings file and enter your SQLAlchemy DB URI (you can also override
default settings as needed)::

  cp settings_local.py.tmpl settings_local.py
  # now edit ...
  vim settings_local.py

.. _Vim: http://www.vim.org/
.. _`GNU Nano`: http://www.nano-editor.org/


.. note::

  Alternatively, if you want your config elsewhere or with different name::

    cp settings_local.py.tmpl {/my/config/file/somewhere}
    export PYBOSSA_SETTINGS={/my/config/file/somewhere}

Create the alembic config file and set the sqlalchemy.url to point to your
database::

  cp alembic.ini.template alembic.ini
  # now set the sqlalchemy.url ...

.. _pybossa-cache:

Installing Redis
================

Since version v0.2.1, PYBOSSA uses Redis not only for caching objects and speed
up the site, but also for limiting the usage of the API requests.

Latest Redis can be installed by downloading the package directly from its
official Redis_ site. Since Ubuntu 14.04 you can also use the internal package::

    sudo apt-get install redis-server

Once you have downloaded it, and installed it, you will need to run two
instances:

* **Redis-server**: as a master node, accepting read and write operations.
* **Redis-sentinel**: as a sentinel node, to configure the master and slave Redis
  nodes.

Server
------
If you have installed the server via your distribution package system, then,
the server will be running already. If this is not the case, check the official
documentation of Redis_ to configure it and run it. The default values should
be fine.

.. note::
    Please, make sure that you are running version >= 2.6

.. note::
    If you have installed the software using the source code, then, check the
    contrib folder, as there is a specific folder for Redis with init.d start
    scripts. You only have to copy that file to /etc/init.d/ and adapt it to
    your needs.

Sentinel
--------
Redis can be run in sentinel mode with the **--sentinel** arg, or by its own
command named: redis-sentinel. This will vary from your distribution and
version of Redis, so check its help page to know how you can run it.

In any case, you will need to run a sentinel node, as PYBOSSA uses it to
load-balance the queries, and also to autoconfigure the master and slaves
automagically.

In order to run PYBOSSA, you will need first to configure a Sentinel node.
Create a config file named **sentinel.conf** with something like this::

    sentinel monitor mymaster 127.0.0.1 6379 2
    sentinel down-after-milliseconds mymaster 60000
    sentinel failover-timeout mymaster 180000
    sentinel parallel-syncs mymaster 1

In the contrib folder you will find a file named **sentinel.conf** that should
be enough to run the sentinel node. Thus, for running it::

    redis-server contrib/sentinel.conf --sentinel

.. note::
    Please, make sure that you are running version >= 2.6

.. note::
    If you have installed the software using the source code, then, check the
    contrib folder, as there is a specific folder for Redis with init.d start
    scripts. You only have to copy that file to /etc/init.d/ and adapt it to
    your needs.

Speeding up the site
====================

Enabling the cache
------------------
PYBOSSA comes with a Cache system that it is enabled by default. PYBOSSA uses
a Redis_ server to cache some objects like projects, statistics, etc. The
system uses the Sentinel_ feature of Redis_, so you can have several
master/slave nodes configured with Sentinel_, and your PYBOSSA server will use
them "automagically".

Once you have started your master Redis-server to accept connections,
Sentinel will manage it and its slaves. If you add a slave, Sentinel will
find it and start using it for load-balancing queries in PYBOSSA Cache system.

For more details about Redis_ and Sentinel_, please, read the official documentation_.

If you want to disable it, you can do it with an environment variable::

    export PYBOSSA_REDIS_CACHE_DISABLED='1'

Then start the server, and nothing will be cached.

.. _Redis: http://redis.io/
.. _Sentinel: http://redis.io/topics/sentinel
.. _documentation: http://redis.io/topics/sentinel

.. note::
   **Important**: We highly recommend you to not disable the cache, as it will boost
   the performance of the server caching SQL queries as well as page views. If
   you have lots of projects with hundreds of tasks, you should enable it.

.. note::
   **Important**: Sometimes Redis is a bit outdated in your Linux distribution.
   If this is the case, you will need to install it by hand, but it is really
   easy and well documented in the official Redis_ site.

Running asynchronous tasks in the background
--------------------------------------------
PYBOSSA uses the Python libraries RQ_ and RQScheduler_ to allow slow or
computationally-heavy tasks to be run in the background in an asynchronous way.

Some of the tasks are run in a periodic, scheduled, basis, like the refreshment
of the cache and notifications sent to users, while others, like the sending of
mails are created in real time, responding to events that may happen inside the
PYBOSSA server, like sending an email with a recovery password.

To allow all this, you will need two additional Python processes to run in the
background: the **worker** and the **scheduler**. The scheduler will create the
periodic tasks while other tasks will be created dynamically. The worker will
execute every of them.

To run the scheduler, just run the following command in a console::

    rqscheduler --host IP-of-your-redis-master-node

Similarly, to get the tasks done by the worker, run::

    python app_context_rqworker.py scheduled_jobs super high medium low email maintenance

It is also recommended the use of supervisor_ for running these processes in an
easier way and with a single command.

.. note::
    While the execution of the scheduler is optional (you will not have the
    improvements in performance given by them, but you may also not need them),
    the execution of the worker is mandatory for the normal functioning of the
    PYBOSSA server, so make sure you run the command for it.

.. _RQ: http://python-rq.org/
.. _RQScheduler: https://github.com/ui/rq-scheduler
.. _supervisor: http://supervisord.org/


Configuring the DataBase
========================

You need first to add a user to your PostgreSQL_ DB::

    sudo su postgres
    createuser -d -P pybossa

Use password ``tester`` when prompted.

.. note::
    You should use the same user name that you have used in the
    settings_local.py and alembic.ini files.

After running the last command, you maybe also have to answer to these questions:

* Shall the new role be a super user? Answer **n** (press the **n** key).
* Shall the new role be allowed to create databases? Answer **y** (press the **y** key).
* Shall the new role be allowed to create more new roles? Answer **n** (press the **n** key).

And now, you can create the database::

    createdb pybossa -O pybossa

Finally, exit the postgresql user::

    exit

Then, populate the database with its tables::

  python cli.py db_create

Run the web server::

  python run.py

Open in your web browser the following URL::

  http://localhost:5000

And if you see the following home page, then, your installation has been
completed:

.. image:: http://i.imgur.com/hPtgo6S.png


Updating PYBOSSA
================

Update PYBOSSA core and migrating the database table structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, the PYBOSSA developers add a new column or table to the PYBOSSA
server, forcing you to carry out a **migration** of the database. PYBOSSA uses
Alembic_ for performing the migrations, so in case that your production server
need to upgrade the DB structure to a new version, all you have to do is to::

  git pull origin master
  pip install -U pip
  pip install -U -r requirements.txt
  alembic upgrade head


The first command will get you the latest source code. Then new libraries are
installed or upgraded. And Alembic is upgrading the database structure.

Very occasionally, updates to the core code will also required pybossa.js_ to 
be updated in your PYBOSSA theme. To update the default theme you can to this::
  
  cd home/pybossa/pybossa/themes/default
  git pull origin master

.. note::
    If you are using the virtualenv_ be sure to activate it before running the
    Alembic_ upgrade command.

.. _Alembic: http://pypi.python.org/pypi/alembic
.. _pybossa.js: https://github.com/Scifabric/pybossa.js


Migrating Your Old DB Records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In versions prior to v0.2.3, HTML was supported as the default option for the
'long_description' field in projects. In new versions of PYBOSSA, Markdown has been
adopted as the default option. However, you can use HTML instead of Markdown
by modifying the default PYBOSSA theme or using your own forked from the default
one.

If you were have been using PYBOSSA for a while you may have projects in your
database whose 'long_description' is in HTML format. Hence, if you are using the
default theme for PYBOSSA you will no longer see them rendered as HTML and may
have some issues.

In order to avoid this, you can run a simple script to convert all the DB project's
'long_description' field from HTML to Markdown, just by running the following
commands::

  pip install -U pip
  pip install -U -r requirements.txt
  python cli.py markdown_db_migrate

The first command will install a Python package that will handle the HTML to
Markdown conversion, while the second one will convert your DB entries.

.. note::
    As always, if you are using the virtualenv_ be sure to activate it before
    running the pip install command.

.. note::
    The latest version of PYBOSSA requires PostgreSQL >= 9.3 as it is using materialized
    views for the dashboard. This feature is only available from PostgreSQL 9.3, so please
    upgrade the DB as soon as possible. For more information about upgrading the PostgreSQL
    database check this page_.

.. _page: http://www.postgresql.org/docs/9.3/static/upgrading.html
