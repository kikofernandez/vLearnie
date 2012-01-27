------------------------------
File Handler (FHY)
------------------------------
In this section you can find the methods that we have built in order to provide 
you with a set of web services for creating your own application.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consult files by username
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Retrieve the file/s information via the given username.

**Arguments**:
  * **username**, your username. 

**Return**::

  [
    {
        "description": "", 
        "title": "Pruebas", 
        "space_id": 1, 
        "file": "files/2011/04/15/Francisco_R._Fernandez_Reyes.png", 
        "pub_date": "2011-02-07", 
        "id": 11
    }, 
    {
    ...
    }
  ]

**URL** http://localhost:8000/api/fhy/<username>/files/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/admin/files/'
  
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consult images by username
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Retrieve the image/s information via the given username.

**Arguments**:
  * **username**, your username. 

**Return**::

  [
    {
        "description": "", 
        "title": "Pruebas", 
        "space_id": 1, 
        "file": "files/2011/04/15/Francisco_R._Fernandez_Reyes.png", 
        "pub_date": "2011-02-07", 
        "id": 11
    }, 
    {
    ...
    }
  ]

**URL** http://localhost:8000/api/fhy/<username>/images/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/admin/images/'

^^^^^^^^^^^^^^^^^^^^^
Consult by space
^^^^^^^^^^^^^^^^^^^^^
Consult the information of the files, images and folders of the given space.

**Arguments**:
  * **space_id**, the id of the space to consult. 

**Return** Return a list of files, images and folders, for instance::
  
  [
    [
        {
            "file": "files/2011/11/05/person.png", 
            "description": "", 
            "space": {
                "id": 1, 
                "user": {
                    "username": "admin", 
                    "first_name": "Kiko", 
                    "last_name": "Fernandez Reyes"
                }, 
                "slug": "mi-primer-espacio", 
                "title": "Mi primer espacio"
            }, 
            "title": "hola", 
            "content_type": {
                "model": "root", 
                "app_label": "fhy", 
                "id": 25, 
                "name": "root"
            }, 
            "pub_date": "2011-11-05", 
            "slug": "hola"
        }
    ], 
    ...
  ]

**URL** http://localhost:8000/api/fhy/<space_id>/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/1/' 


^^^^^^^^^^^^^^^^^^^^^^^^
Consult file by id
^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve the file/s information. If the **id** is given, then we will return 
the information for that specific item.

**Arguments**:
  * **id**, the id of the resource (**optional**).

**Return**::

  {
    "file": "files/2011/11/05/person.png", 
    "description": "", 
    "space": {
        "id": 1, 
        "user": {
            "username": "admin", 
            "first_name": "Kiko", 
            "last_name": "Fernandez Reyes"
        }, 
        "slug": "mi-primer-espacio", 
        "title": "Mi primer espacio"
    }, 
    "title": "hola", 
    "content_type": {
        "model": "root", 
        "app_label": "fhy", 
        "id": 25, 
        "name": "root"
    }, 
    "pub_date": "2011-11-05", 
    "slug": "hola"
  }

**URL** http://localhost:8000/api/fhy/file/<id>/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/file/52/'


^^^^^^^^^^^^^^^^^^^^^^^^
Consult image by id
^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve the image/s information. If the **id** is given, then we will return 
the information for that specific item.

**Arguments**:
  * **id**, the id of the resource (**optional**).

**Return**::

  {
    "file": "files/2011/11/05/person.png", 
    "description": "", 
    "space": {
        "id": 1, 
        "user": {
            "username": "admin", 
            "first_name": "Kiko", 
            "last_name": "Fernandez Reyes"
        }, 
        "slug": "mi-primer-espacio", 
        "title": "Mi primer espacio"
    }, 
    "title": "hola", 
    "content_type": {
        "model": "root", 
        "app_label": "fhy", 
        "id": 25, 
        "name": "root"
    }, 
    "pub_date": "2011-11-05", 
    "slug": "hola"
  }

**URL** http://localhost:8000/api/fhy/image/<id>/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/image/52/'

^^^^^^^^^^^^^^^^^^^^^^^^
Create file
^^^^^^^^^^^^^^^^^^^^^^^^

Create a new file

**Arguments**:
  * **title**, the title for the file.
  * **space**, the id of the space.
  * **file**, the file to upload.
  * **description**, the description of the file.
  * **pub_date**, the publication date in the format 'YYYY-MM-DD'. 

**Return** True

**URL** http://localhost:8000/api/fhy/file/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/file/' -X POST -F 'title=hola' -F 'space=1' -F 'file=@/Users/kikofernandezrey/Desktop/person.png' 

^^^^^^^^^^^^^^^^^^^^^^^^
Create image
^^^^^^^^^^^^^^^^^^^^^^^^

Upload a new image

**Arguments**:
  * **title**, the title for the image.
  * **space**, the id of the space.
  * **file**, the file to upload.
  * **description**, the description of the image.
  * **pub_date**, the publication date in the format 'YYYY-MM-DD'. 

**Return** True

**URL** http://localhost:8000/api/fhy/image/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/image/' -X POST -F 'title=hola' -F 'space=1' -F 'file=@/Users/kikofernandezrey/Desktop/person.png' 

^^^^^^^^^^^^^^^^^^^^^^^^
Update file
^^^^^^^^^^^^^^^^^^^^^^^^

Update the given file

**Arguments**:
  * **title**, the title for the file.
  * **file**, the file to upload.
  * **description**, the description of the file.
  * **pub_date**, the publication date in the format 'YYYY-MM-DD'. 

**Return** True

**URL** http://localhost:8000/api/fhy/file/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/file/' -F 'title=hola' -X PUT 
  
^^^^^^^^^^^^^^^^^^^^^^^^
Update image
^^^^^^^^^^^^^^^^^^^^^^^^

Update the given image

**Arguments**:
  * **title**, the title for the image.
  * **file**, the file to upload.
  * **description**, the description of the file.
  * **pub_date**, the publication date in the format 'YYYY-MM-DD'. 

**Return** True

**URL** http://localhost:8000/api/fhy/image/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/image/' -F 'title=hola' -X PUT 


^^^^^^^^^^^^^^^^^^^^^^^^
Delete file
^^^^^^^^^^^^^^^^^^^^^^^^

Delete the given file

**Arguments**:
  * **id**, the id of the file. 

**Return** True

**URL** http://localhost:8000/api/fhy/file/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/file/55/' -X DELETE 
  
^^^^^^^^^^^^^^^^^^^^^^^^
Delete image
^^^^^^^^^^^^^^^^^^^^^^^^

Delete the given image

**Arguments**:
  * **id**, the id of the image. 

**Return** True

**URL** http://localhost:8000/api/fhy/image/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/image/file/55/' -X DELETE 

^^^^^^^^^^^^^^^^^
Delete file
^^^^^^^^^^^^^^^^^

Delete the given file.

**Arguments**:
  * **id**, the id of the file resource to delete.

**Return** True

**URL** http://localhost:8000/api/fhy/delete_file/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/delete_file/1/'
  
^^^^^^^^^^^^^^^^^
Delete image
^^^^^^^^^^^^^^^^^

Delete the given image.

**Arguments**:
  * **id**, the id of the image resource to delete.

**Return** True

**URL** http://localhost:8000/api/fhy/delete_image/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/fhy/delete_image/1/'
  
  