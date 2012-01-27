--------------
Portfolio
--------------
In this section you can find the methods for interacting with the **Portfolio API web services**.

^^^^^^^^^^^^^^^^^^^^^
Get portfolio
^^^^^^^^^^^^^^^^^^^^^
Get the portfolio information based on the given **id** or get all the portfolios.

**Arguments**:
  * **id**, the given id to consult (**optional**).

**Return**::

  [
    ...,
    {
        "first_name": "Jose", 
        "last_name": "Garcia", 
        "bio_html": "Soy un estudiante de la ETSII de la Universidad de Málaga y estoy cerca de finalizar la carrera de Ingenieria Superior en Informática.", 
        "birthday": "1985-11-02", 
        "user": {
            "username": "alumno", 
            "first_name": "Jose", 
            "last_name": "Garcia", 
            "id": 2
        }, 
        "id": 3
    }
  ]
    
**URL**::
  
  http://localhost:8000/api/portfolio/pinformation/

  http://localhost:8000/api/portfolio/pinformation/2/


**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/pinformation/'

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create portfolio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create the portfolio for the user

**Arguments**:
  * **first_name**, the first name of the user.
  * **last_name**, the last name of the user.
  * **birthday**, the birthday (**optional**).
  * **current_address**, the current address (**optional**).
  * **bio**, a small description of the user's life (**optional**).

**Return**::

    {
        "first_name": "Jose", 
        "last_name": "Garcia", 
        "birthday": "1985-11-02", 
        "user": {
            "username": "alumno", 
            "first_name": "Jose", 
            "last_name": "Garcia", 
            "id": 2
        }, 
        "id": 3
    }
    
**URL** http://localhost:8000/api/portfolio/pinformation/


**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/pinformation/' -F 'first_name=Jose' -F 'last_name=Garcia' -F 'birthday=1985-11-02' -X POST


^^^^^^^^^^^^^^^^^^^^^^^^
Update portfolio
^^^^^^^^^^^^^^^^^^^^^^^^
Update the portfolio given the **id**.

**Arguments**:
  * **first_name**, the first name of the user (**optional**).
  * **last_name**, the last name of the user (**optional**).
  * **birthday**, the birthday (**optional**).
  * **current_address**, the current address (**optional**).
  * **bio**, a small description of the user's life (**optional**).

**Return** True

**URL** http://localhost:8000/api/portfolio/pinformation/<id>/


**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/pinformation/2/' -F 'first_name=Jose' -X PUT


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete portfolio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete the given portfolio (obviously if you are the owner).

**Arguments**:
  * **id**, the **id** of the portfolio.

**Return** True

**URL** http://localhost:8000/api/portfolio/pinformation/<id>/


**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/pinformation/2/' -X DELETE




^^^^^^^^^^^^^^^^^^^^^
Get studies
^^^^^^^^^^^^^^^^^^^^^
Get the studies of the given person (**id** or **username**) or the studies of all the users.

**Arguments**:
  * **id**, the given id to consult (**optional**).
  * **username**, the username of the person (**optional**).

**Return**::

  [
    {
        "end": "2009-06-23", 
       "speciality": "Los cursos que realice fueron principalmente del Master de Ciencias Computacionales donde aprendi principalmente IA mediante logica epistemica y administracion de proyectos. Logica epistemica, Programacion PHP", 
        "title": "Beca Erasmus", 
        "id": 4, 
        "start": "2008-09-11", 
        "place": "Universidad de Luxemburgo", 
        "user_id": 2, 
        "additional_info": ""
    }, 
    ...
  ]
    
**URL**::
  
  http://localhost:8000/api/portfolio/studies/

  http://localhost:8000/api/portfolio/studies/<id>/

  http://localhost:8000/api/portfolio/studies/<username>/


**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/studies/2/'

  curl -u admin:1234 'http://localhost:8000/api/portfolio/studies/kiko/'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add a new study.

**Arguments**:
  * **place**, the place where you studied.
  * **title**, the title that you got after your studies.
  * **start**, the date when you started (**format: YYYY-MM-DD**).
  * **end**, the date when you finished (**optional**).
  * **speciality**, your specialities (**optional**).
  * **additional_info**, additional info if necessary (**optional**).

**Return**::

     {
        "end": "2009-06-23", 
        "speciality": "Los cursos que realice fueron principalmente del Master de Ciencias Computacionales donde aprendi principalmente IA mediante logica epistemica y administracion de proyectos. Logica epistemica, Programacion PHP", 
        "title": "Beca Erasmus", 
        "id": 4, 
        "start": "2008-09-11", 
        "place": "Universidad de Luxemburgo", 
        "user_id": 2, 
        "additional_info": ""
    }

**URL** http://localhost:8000/api/portfolio/studies/


**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/studies/' -F 'title=Beca Erasmus' -F 'place=Universidad de Luxemburgo' -F 'start=2008-09-11' -F 'end=2009-06-23' -F 'speciality=...' -X POST


^^^^^^^^^^^^^^^^^^^^^^^^
Update studies
^^^^^^^^^^^^^^^^^^^^^^^^
Update the studies given the **id** of the object to change.

**Arguments**:
  * **place**, the place where you studied (**optional**).
  * **title**, the title that you got after your studies (**optional**).
  * **start**, the date when you started (**format: YYYY-MM-DD) (**optional**).
  * **end**, the date when you finished (**optional**).
  * **speciality**, your specialities (**optional**).
  * **additional_info**, additional info if necessary (**optional**).

**Return**::

   {
        "end": "2009-06-23", 
        "speciality": "Los cursos que realice fueron principalmente del Master de Ciencias Computacionales donde aprendi principalmente IA mediante logica epistemica y administracion de proyectos. Logica epistemica, Programacion PHP", 
        "title": "Beca Erasmus", 
        "id": 4, 
        "start": "2008-09-11", 
        "place": "Universidad de Luxemburgo", 
        "user_id": 2, 
        "additional_info": "Nada mas"
    }


**URL** http://localhost:8000/api/portfolio/studies/<id>/


**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/studies/4/' -F 'additional_info=Nada más' -X PUT


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete the given study (obviously if you are the owner).

**Arguments**:
  * **id**, the **id** of the study.

**Return** True

**URL** http://localhost:8000/api/portfolio/studies/<id>/


**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/studies/4/' -X DELETE





^^^^^^^^^^^^^^^^^^^^^
Get projects
^^^^^^^^^^^^^^^^^^^^^
Get project/s given the **id** or **username**. Otherwise, the projects of all the users.

**Arguments**:
  * **id**, the given id to consult (**optional**).
  * **username**, the username of the person (**optional**).

**Return**::
  
  [
    {
        "category": {
            "user": {
                "username": "alumno", 
                "first_name": "Jose", 
                "last_name": "Garcia", 
                "id": 2
            }, 
            "name": "nueva", 
            "id": 1
        }, 
        "end_date": "2011-05-25", 
        "name": "MSF", 
        "url": "", 
        "user": {
            "username": "alumno", 
            "first_name": "Jose", 
            "last_name": "Garcia", 
            "id": 2
        }, 
        "id"=3,
        "start_date": "2011-05-25", 
        "pull_quote": "", 
        "short_description": "Colaboracion realizada para MSF.", 
        "slug": "msf", 
        "description": "asdasdasd aasdasd"
    },
    ...
  ]
    
**URL**::
  
  http://localhost:8000/api/portfolio/project/

  http://localhost:8000/api/portfolio/project/<id>/

  http://localhost:8000/api/portfolio/project/<username>/


**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/project/2/'

  curl -u admin:1234 'http://localhost:8000/api/portfolio/project/kiko/'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add a new project.

**Arguments**:
  * **start_date**, the date when you started (**format: YYYY-MM-DD**).
  * **end_date**, the date when you finished (**optional**).
  * **name**, name of the project.
  * **category**, category of the project.
  * **url**, URL of the project (**optional**).
  * **pull_quote**, what they said (**optional**).
  * **short_description**, a short description of the project (**optional**).
  * **description**, the description of the project (**optional**).

**Return**::

    {
        "category": {
            "user": {
                "username": "alumno", 
                "first_name": "Jose", 
                "last_name": "Garcia", 
                "id": 2
            }, 
            "name": "nueva", 
            "id": 1
        }, 
        "end_date": "2011-05-25", 
        "name": "MSF", 
        "url": "", 
        "user": {
            "username": "alumno", 
            "first_name": "Jose", 
            "last_name": "Garcia", 
            "id": 2
        }, 
        "id"=3,
        "start_date": "2011-05-25", 
        "pull_quote": "", 
        "short_description": "Colaboracion realizada para MSF.", 
        "slug": "msf", 
        "description": "asdasdasd aasdasd"
    }

**URL** http://localhost:8000/api/portfolio/project/


**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/project/' -F 'start_date=2011-05-25' -F 'end_date=2011-05-25' -F 'short_description=Colaboracion realizada para MSF' -F 'description=asdasdasd aasdasd' -F 'category=1' -X POST


^^^^^^^^^^^^^^^^^^^^^^^^
Update project
^^^^^^^^^^^^^^^^^^^^^^^^
Update the project given the **id** of the object to change.

**Arguments**:
  * **start_date**, the date when you started (**format: YYYY-MM-DD**) (**optional**).
  * **end_date**, the date when you finished (**optional**).
  * **name**, name of the project (**optional**).
  * **category**, category of the project (**optional**).
  * **url**, URL of the project (**optional**).
  * **pull_quote**, what they said (**optional**).
  * **short_description**, a short description of the project (**optional**).
  * **description**, the description of the project (**optional**).

**Return**::

   {
        "category": {
            "user": {
                "username": "alumno", 
                "first_name": "Jose", 
                "last_name": "Garcia", 
                "id": 2
            }, 
            "name": "nueva", 
            "id": 1
        }, 
        "end_date": "2011-05-25", 
        "name": "MSF", 
        "url": "", 
        "user": {
            "username": "alumno", 
            "first_name": "Jose", 
            "last_name": "Garcia", 
            "id": 2
        },
        "id"=3,
        "start_date": "2011-05-25", 
        "pull_quote": "", 
        "short_description": "Colaboracion realizada para MSF.", 
        "slug": "msf", 
        "description": "Cambio"
    }



**URL** http://localhost:8000/api/portfolio/project/<id>/


**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/project/3/' -F 'description=Cambio' -X PUT


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete the given project (obviously if you are the owner).

**Arguments**:
  * **id**, the **id** of the project.

**Return** True

**URL** http://localhost:8000/api/portfolio/project/<id>/


**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/project/3/' -X DELETE







^^^^^^^^^^^^^^^^^^^^^
Get skills
^^^^^^^^^^^^^^^^^^^^^
Get the skills given by the **id** or **username**. Otherwise, the skills of all the users.

**Arguments**:
  * **id**, the given id to consult (**optional**).
  * **username**, the username of the person (**optional**).

**Return**::
  
  [
    {
        "user": {
            "username": "kiko", 
            "first_name": "Kiko", 
            "last_name": "Fernandez", 
            "id": 3
        }, 
        "name": "sadsdf", 
        "id": 4
    },
       ...
  ]
    
**URL**::
  
  http://localhost:8000/api/portfolio/skill/

  http://localhost:8000/api/portfolio/skill/<id>/

  http://localhost:8000/api/portfolio/skill/<username>/


**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/skill/2/'

  curl -u admin:1234 'http://localhost:8000/api/portfolio/skill/kiko/'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add skill
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add a new skill to your portfolio. 

**Arguments**:
  * **name**, the name of your skill.

**Return**::

    {
        "user": {
            "username": "kiko", 
            "first_name": "Kiko", 
            "last_name": "Fernandez", 
            "id": 3
        }, 
        "name": "invisibility", 
        "id": 4
    }
   
**URL** http://localhost:8000/api/portfolio/skill/


**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/skill/' -F 'name=invisibility' -X POST


^^^^^^^^^^^^^^^^^^^^^^^^
Update skill
^^^^^^^^^^^^^^^^^^^^^^^^
Update the skill given the **id** of the object to change.

**Arguments**:
  * **name**, change the name (**optional**).

**Return**::

    {
        "user": {
            "username": "kiko", 
            "first_name": "Kiko", 
            "last_name": "Fernandez", 
            "id": 3
        }, 
        "name": "OOP", 
        "id": 4
    }
  


**URL** http://localhost:8000/api/portfolio/skill/<id>/


**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/skill/4/' -F 'name=OOP' -X PUT


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete skill
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete the given skill (obviously if you are the owner).

**Arguments**:
  * **id**, the **id** of the skill.

**Return** True

**URL** http://localhost:8000/api/portfolio/skill/<id>/


**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/portfolio/skill/4/' -X DELETE

