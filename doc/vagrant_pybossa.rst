======================================
Testing PYBOSSA with a Virtual Machine
======================================

`Vagrant`_ is an open source solution that allows you to create and configure 
lightweight, reproducible, and portable development environments.

Vagrant_ simplifies a lot setting up all the requirements for a web application
like PYBOSSA, as you will set up a virtual machine that *automagically*
downloads all the required libraries and dependencies for developing and
testing the project.

For these reasons, PYBOSSA uses Vagrant to allow you to start hacking the
system in a very simple way, and more importantly, without polluting your
system with lots of libraries that you may or may not needed (everything is
configured in the Virtual Machine, which is a very safe sand-box!).

Additionally several cloud companies have integration with Vagrant, so
deploying a PYBOSSA server is really simple using this method.


.. note::

    The virtual machine and server are configured with a **very basic
    security**
    set of rules (passwords, secrets, firewall, etc.). Therefore, *if you are going to
    use this method to deploy a PYBOSSA production server* **it is your responsibility
    to secure the system properly**.

Setting up PYBOSSA with Vagrant
===============================

In order to start using Vagrant and PYBOSSA all you have to do is installing
the following open source software:

#. VirtualBox_ (min version 4.2.10)
#. Vagrant_ (min version 1.2.1)

.. note::
    Vagrant_ and VirtualBox_ works in Windows, GNU/Linux and Mac OS X, so you can try and run
    PYBOSSA without problems!

Clone the PYBOSSA git repository (be sure to install git in your
machine!)::

    $ git clone --recursive https://github.com/Scifabric/pybossa.git

Once the source code has been downloaded, all you have to do to start your
PYBOSSA development environment is typing the following::

    $ cd pybossa
    $ vagrant up

The system will download a Virtual Machine, install all the required libraries
for PYBOSSA and set up the system for you inside the Virtual Machine.

Vagrant is really great, because all the changes that you will make in your
local copy of PYBOSSA will be automatically populated to the Virtual Machine.
Hence, if you add a new feature to the system, you will be able to test it
right away (this feature is pretty handy for workshop, hackfests, etc.).

Running the PYBOSSA server
==========================

Now that all the libraries and dependencies have been installed, you can lunch
the PYBOSSA development server::

  $ vagrant ssh
  $ python run.py

.. note::
    Virtualenv (located in /home/vagrant/pybossa-env) is always activated on login.

Now all you have to do is open the following URL in your web browser::

  http://127.0.0.1:5000

And you are done! Happy Hacking!

.. note::

    PYBOSSA needs a RQ worker process. It is running by default permanently in
    the background in the VM and is controlled by supervisor.
    Optional is also the RQ scheduler process for speeding up tasks like
    ZIP creation. This process is off by default now.
    If you are developing on RQ worker you want to restart or disable it with
    supervisorctl.

.. _`Vagrant`: http://www.vagrantup.com/
.. _`VirtualBox`: https://www.virtualbox.org/
