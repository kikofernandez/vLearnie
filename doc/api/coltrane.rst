-------------
Coltrane
-------------

^^^^^^^^^^^^^^^^^^^^^
Get post by author
^^^^^^^^^^^^^^^^^^^^^
Get a list of entries based on the author name

**Arguments**:
  * **author**, the name of the author.
  * **space**, the id of the space (**optional**).
  * **pub_date**, the publication date following the format *YYYY-MM-DD* (**optional**).

**Return**::

  [
    {
        "body": "aasdasdads afafd", 
        "author": {
            "username": "admin", 
            "first_name": "Kiko", 
            "last_name": "Fernandez Reyes", 
            "id": 1
        }, 
        "space": {
            "id": 5, 
            "title": "prueba"
        }, 
        "title": "nueva", 
        "pub_date": "2011-06-10", 
        "id": 6
    }
  ]


**URL**:: 
  http://localhost:8000/api/blog/<author>/
  
  http://localhost:8000/api/blog/<author>/<space_id>/

  http://localhost:8000/api/blog/<author>/<space_id>/<pub_date>/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/blog/admin/'

  curl -u admin:1234 'http://localhost:8000/api/blog/admin/5/'

  curl -u admin:1234 'http://localhost:8000/api/blog/admin/5/2011-11-02'


^^^^^^^^^^^^^^^^^
Get post by id
^^^^^^^^^^^^^^^^^
Using this web service you can get all your entries or just the one with the given **id**.

**Arguments**:
  * **id**, **optional argument** where you specify the entry that you want yo retrieve. If you do not provide an **id** argument, then all your entries will be got.

**Return** Either a JSON list of elements (if the **id** field was not provided) or a JSON object which is the entry::

  [
    {
        "body": "Afortunado yo", 
        "author": {
            "username": "admin", 
            "first_name": "Kiko", 
            "last_name": "Fernandez Reyes", 
            "id": 1
        }, 
        "space": {
            "id": 6, 
            "title": "Otra prueba"
        }, 
        "title": "Soy afortunado", 
        "pub_date": "2011-11-03", 
        "id": 18
    }, 
    {
        "body": "Esto es otra entrada", 
	...
    }
   ]



**URL** http://localhost:8000/api/blog/ or http://localhost:8000/api/blog/<id>/

**Method** GET

**Example**::
  
  curl -u <username>:<password> 'http://localhost:8000/api/blog/'

  curl -u <username>:<password> 'http://localhost:8000/api/blog/<id>/' -F 'id=<given-id>'

^^^^^^^^^^^^^^^^^
Create entry
^^^^^^^^^^^^^^^^^
Create an entry given the information

**Arguments**:
  * **spaceid**, the **spaceid** for the entry to belong to.
  * **title**, the title for the entry.
  * **body**, the body for the entry.
  * **tags**, the tags for the entry.
  * **status**, **optional paramenter**, if this is not supplied the default status is **LIVE**.
  * **pub_date**, the publication date with the following format::

      YYYY-MM-DD: 2012-12-12

**Return**::

  {
    "body": "Hola como estamos", 
    "author": {
        "username": "admin", 
        "first_name": "Kiko", 
        "last_name": "Fernandez Reyes", 
        "id": 1
    }, 
    "space": {
        "id": 6, 
        "title": "Otra prueba"
    }, 
    "title": "Hola hola", 
    "pub_date": "2011-12-24", 
    "id": 19
   }  

**URL** http://localhost:8000/api/blog/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/blog/' -F 'spaceid=6' -F 'title=Hola hola' -F 'body=Hola como estamos' -F 'tags=que, tal' -F 'pub_date=2011-12-24' -X POST

^^^^^^^^^^^^^^^^^^^^^
Update entry by id
^^^^^^^^^^^^^^^^^^^^^
Update the entry base on the given **id**.

**Arguments**:
  * **spaceid**, the **spaceid** for the entry to belong to (**optional**).
  * **title**, the title for the entry (**optional**).
  * **body**, the body for the entry (**optional**).
  * **tags**, the tags for the entry (**optional**).
  * **status**, **optional paramenter**, if this is not supplied the default status is **LIVE** (**optional**).
  * **pub_date**, the publication date (**optional**) with the following format::

      YYYY-MM-DD: 2012-12-12

**Return**::

  {
    "body": "Hola como estamos", 
    "author": {
        "username": "admin", 
        "first_name": "Kiko", 
        "last_name": "Fernandez Reyes", 
        "id": 1
    }, 
    "space": {
        "id": 6, 
        "title": "Otra prueba"
    }, 
    "title": "Hola holaaa", 
    "pub_date": "2011-12-24", 
    "id": 19
   }  

**URL** http://localhost:8000/api/blog/<id>/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/blog/19/' -F 'title=Hola holaaa' -X PUT

^^^^^^^^^^^^^^^^^^^^^
Delete entry by id
^^^^^^^^^^^^^^^^^^^^^
Delete the given entry by the **id**.

**Arguments**:
  * **id**, the id of the entry.

**Return** True

**URL** http://localhost:8000/api/blog/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/blog/19/' -X DELETE

