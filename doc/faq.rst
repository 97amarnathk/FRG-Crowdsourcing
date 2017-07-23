==========================
Frequently Asked Questions
==========================

.. note::
    If you do not find your question in this section, please send it to us
    directly to *info AT pybossa DOT com*. We will try to help you and add your
    question to the FAQ.

Users
=====
Do I need to create an account to participate in the project?
-------------------------------------------------------------
It depends. The owners of the projects can disable anonymous contributions
(usually due to privacy issues with the data), forcing you to create an account
if you want to contribute to that specific project.


Projects
========
How can I create a project?
--------------------------------
You can create a project using web forms, or if you prefer it using the
API. We recommend you to read the :doc:`user/overview` and :doc:`user/tutorial` 
sections.

Can I disable anonymous contributions?
--------------------------------------
Yes, you can. Check your project settings and toggle the drop down menu:
*Allow Anonymous Contributors* from Yes to No. Check the :ref:`project-details`
for further information.

Can I create *golden tasks*?
----------------------------
Yes, you can. PYBOSSA has a field for every Task named: *calibration* that will
identify the task as a *golden* task or as we call them as a *calibration
task*. Calibration tasks can be used to weight the answers of the volunteers
(authenticated and anonymous) as you know the answer for those given tasks. For
example, if a user has answered all the calibration tasks correctly you can
give a weight of 1 point to all his/her answers, while if the user only
answered 50% of them correctly, the answers for the rest of the tasks could be
given a weight of 0.5 points.

Can I delete my project and all the task and task runs?
-----------------------------------------------------------
Yes, you can. If you are the owner of the project you can delete the
project, and automatically all the task and associated task runs will be
deleted (**note**: this cannot be undone!). Check the :ref:`project-delete` section
for further details.

Do you provide any statistics about the users for my project?
-----------------------------------------------------------------
Yes, every project has its own statistics page that shows information about
the distribution of answers per type of user, an estimation about how long it
will take to complete all your tasks, the top 5 authenticated and anonymous
users, etc. Check the *Statistics* link in the left local sidebar of your
project.

My project is not getting too much attention, how can it be a *featured* project?
---------------------------------------------------------------------------------
Featured projects are managed by the administrators of the site. Contact
them about this issue, and they will decide about your project.

I have all my data in a CSV file, can I import it?
--------------------------------------------------
Yes, you can. PYBOSSA supports the CSV format, so all you have to do is upload
your file to a file server like DropBox, copy the public link and paste it in
the importer section. PYBOSSA also supports Google Drive Spreadsheets, see
:ref:`csv-import` section for further details.

My data is in a Google Doc Spreadsheet, can I import the data into my project?
--------------------------------------------------------------------------
Yes, you can. PYBOSSA supports the Google Drive Spreadsheets, so make it
public, copy the link and use that link to import it the Google Drive importer
section. See :ref:`csv-import` section for further details.

All my tasks have been completed, how do I download the results to analyze them?
--------------------------------------------------------------------------------
You can export all the data of your project whenever you want. The data can
be exported directly from the *Tasks* section (check the *Tasks* link in the
left sidebar of your project and click in the export box). PYBOSSA can
export your tasks and task runs (or answers) to a CSV file, JSON format or to
a CKAN server. See the :ref:`export-results` section for further details.

What is a Task Run?
-------------------
A Task Run is a submitted answer sent by one user (authenticated or anonymous)
to one of the tasks of your project. In other words, it is the work done by
one volunteer for one task.

What is the Task Presenter?
---------------------------
The task presenter is the web project that will load the tasks of your
project and present them to the user. It is an HTML + JavaScript
project. See the :ref:`task-presenter` section for further details.

PYBOSSA
=======
Does PYBOSSA have an API?
-------------------------
Yes, it does. PYBOSSA has a :ref:`api` that allows you to create projects,
download results, import tasks, etc. Please see the :ref:`api` section for more
details and the :doc:`user/tutorial` for a full example about how you can use
it.

Is PYBOSSA open-source?
-----------------------
Yes, it is. PYBOSSA is licensed under the `GNU Affero general public license
version 3.0`_. 

.. _`GNU Affero general public license version 3.0`: http://www.gnu.org/licenses/agpl-3.0.html

Do you provide project templates or examples projects?
------------------------------------------------------
Yes, we do. You can find several open source project examples that can be
re-used for image/sound pattern recognition problems, geo-coding, PDF transcription, 
etc. Check the official `Git repository`_ for all the available projects.

.. _`Git repository`: http://github.com/Scifabric/

Support
=======

PYBOSSA is free and open source, that means that anyone can create a project and 
benefit from the endless features that PYBOSSA has to offer, so that you can reach 
your ultimate goal. And the best part? That it is free of charge! 

As well as the FAQs and all the available documentation to help you create and 
develop your PYBOSSA project, we will be happy to answer your questions related 
to the running of PYBOSSA in general. 

Scifabric offers different options for support. Check them and use the one that fits
your needs: http://pybossa.com/support/
