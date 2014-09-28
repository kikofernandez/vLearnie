[![Codacy Badge](https://www.codacy.com/project/badge/235f5856e72a434193d67ea897196047)](https://www.codacy.com)
vLearnie
==========

This software provides you with a multi-user portfolio system, with a clean and simple user interface.

Specifications
----------------
The following is a list of the current features that are implemented:

* The user can create his own **Personal Spaces**
* **Blog system** based on personal spaces, for each personal space the user will have a new blog system
* **Link area** where you can keep track of your favorite links
* **Portfolio system** where the user can add personal information, studies and projects / work done.
* **Virtual Filesystem** where the user can create virtual folders and upload his files.
* **Community**, similar to a forum but the users can publish articles inside every community. Every community has a built-in support for RSS and Atom.
* **Permission control manager**, where the user can select what people from the system can look at his blog/s.
* **Integration within Moodle**, it offers integration with Moodle sharing the Moodle session file.
* **RESTful web service API included**, it has a RESTful API of web services that we built using the Piston framework. You can pretty much have the same functionality as the platform using these web services.

Instalation
------------

If you are using this application as a stand-alone application, then you have to download the project, go to the file **vLearnie/msf/settings.py** and do the modifications if any, and run the server::

    $> python manage.py syncdb
    
    $> python manage.py runserver

Platform Documentation
-----------------------
More documentation about the platform and how to use the RESTful web service API can be found at: **vLearnie/doc/_built/html/index.html**

Dependencies
--------------

List of dependencies:

* Markdown==2.0.3
* MySQL-python==1.2.3
* PIL==1.1.7
* SQLAlchemy==0.6.6
* Sphinx==1.0.7
* django-piston==0.2.2
* django-tagging==0.3.1

Demo
-----
Demo at http://vimeo.com/35751402
