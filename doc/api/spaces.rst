------------------
Spaces
------------------
In this section you can find the methods that we have built in order to provide 
you with a set of web services for creating your own application.

^^^^^^^^^^^^^^^^^^^^
Get user spaces
^^^^^^^^^^^^^^^^^^^^
Consult your own spaces.


**Arguments**:
  * **id**, optional argument.

**Return**::

  [
    {
        "id": 1, 
        "user": {
            "username": "admin", 
            "first_name": "Kiko", 
            "last_name": "Fernandez Reyes"
        }, 
        "slug": "mi-primer-espacio", 
        "title": "Mi primer espacio"
    }, 
    ...
  ]

**URL** http://localhost:8000/api/space/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/space/'

^^^^^^^^^^^^^^^^^^^^
Create user space
^^^^^^^^^^^^^^^^^^^^
Create a new space.


**Arguments**:
  * **title**, the given title.

**Return**::

  {
      "id": 1, 
      "user": {
          "username": "admin", 
          "first_name": "Kiko", 
          "last_name": "Fernandez Reyes"
      }, 
      "slug": "mi-primer-espacio", 
      "title": "Mi primer espacio"
  }

**URL** http://localhost:8000/api/space/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/space/' -F 'title=LTO' -X POST

^^^^^^^^^^^^^^^^^^^^
Update user space
^^^^^^^^^^^^^^^^^^^^
Update the given space.

**Arguments**:
  * **id**, the given user space to change.
  * **title**, the given title.

**Return**::

  {
      "id": 1, 
      "user": {
          "username": "admin", 
          "first_name": "Kiko", 
          "last_name": "Fernandez Reyes"
      }, 
      "slug": "mi-primer-espacio", 
      "title": "Mi primer espacio"
  }

**URL** http://localhost:8000/api/space/<id>/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/space/1/' -F 'title=LTO' -X PUT