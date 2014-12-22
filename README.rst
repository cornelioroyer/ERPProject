============
ERP Poject
============

ERPProject is an Enterprise Resource Planning Project has 7 businnes module and developed by 7 student group named SOLATE, and now them a bachelor degree of Universitas Trunojoyo Madura.

modules that have been developed is:
====================================

* Procurement Module by Reiza Judiz Pradana (judiz_7777@live.com)
* Financial Accounting by Achmad Afiffudin Nurzein (afifnz@gmail.com)
* CRM and Distribution Module by Farid Ilham Al-qorni (djokers10@gmail.com)
* Manufacturing Module by Ja'far Assodiq (fhutm.madani13jafar@gmail.com)
* Asset Management Module by Zaenal Arifin (enalfagundes@yahoo.com)
* Human Resource Module by Fery Febriansyah (fefeland91@gmail.com)
* Inventory Module by Rhiyananta Catur (master.rhiyan@gmail.com)

The Application is the result of the research, after doing research in PT. IGLAS (Persero), that the company is Indonesian Glass packaging industri. so the business process of the application is following business process in the company.

Thank a lot:
* Mr. Hermawan (hermawan.unijoyo@gmail.com)
* Miss Rika Yunitarini (rika-yunitarini@yahoo.com)

Install
=======
First of all you obviously need to clone this project locally, so you must install git application on your machine. 
`git clone https://github.com/darklow/django-suit.git`

Python
======
You must install python on your machine, because the base of programming in this application using python.
`sudo apt-get install python`
automatically your machine will installed 2.7 python version

Virtual Enveronment
==================
our suggestion for you, to make a python virtual enveronment. the enveronment make you easiely to developing the application.
see the `virtual enveronment docs <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

Django & Python modules
======================

* Setup a new virtual env and activate it.
* `pip install -r requirement.txt` to install the correct version of Django

Database
========

Default, the database of application using SQLite Database. but you can changing the database with PostgreSQL if you want, with little configuring in setting.py file.

`./manage.py syncdb` to make a database automatically, without write line by line Database Code. It's Simple =)

Running the project
===================

To run this project you will have to run:
* `./manage.py runserver` to running the server.
* than open your browser and insert url `127.0.0.1:8000`.
* installation  done and the application already running. =)
