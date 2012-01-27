-----------------
Community
-----------------

^^^^^^^^^^^^^^^^^^^^
Get communities
^^^^^^^^^^^^^^^^^^^^
Get the list of communities.

**Arguments**:
  * **id**, **optional** argument for getting the information for a specific community.

**Return**::

  [
    {
        "id": 1, 
        "excerpt": "", 
        "description": "Comunidad donde poder extender el contenido de LTO", 
        "title": "LTO"
    }, 
    {
        "id": 4, 
        "excerpt": "", 
        "description": "", 
        "title": "Introduccion al uso de comunidades"
    }
  ]


**URL** http://localhost:8000/api/community/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/'

^^^^^^^^^^^^^^^^^^^^
Create community
^^^^^^^^^^^^^^^^^^^^
Create a new community.

**Arguments**:
  * **title**, the title of the community.
  * **excerpt**, a brief description of the topic.
  * **description**, the description for the community.

**Return**::

  {
    "id": 5, 
    "excerpt": "Pruebas", 
    "description": "Vamos a realizar unas pruebas", 
    "title": "Pruebas"
  }


**URL** http://localhost:8000/api/community/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/' -F 'title=Pruebas' -F 'excerpt=Pruebas' -F 'description=Vamos a realizar una pruebas' -X POST

^^^^^^^^^^^^^^^^^^^^
Update community
^^^^^^^^^^^^^^^^^^^^
Updates the given community.

**Arguments**:
  * **id**, the id of the community to change.
  * **title**, the title of the community (**optional**).
  * **excerpt**, a brief description of the topic (**optional**).
  * **description**, the description for the community (**optional**).

**Return**::

  {
    "id": 5, 
    "excerpt": "Pruebas", 
    "description": "Vamos a realizar unas pruebas", 
    "title": "Pruebas"
  }


**URL** http://localhost:8000/api/community/<id>/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/5/' -F 'title=Pruebas' -X PUT

^^^^^^^^^^^^^^^^^^^^
Delete community
^^^^^^^^^^^^^^^^^^^^
Delete the given community.

**Arguments**:
  * **id**, the id of the community to delete.

**Return** True

**URL** http://localhost:8000/api/community/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/'5/ -X DELETE

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Get resources by community
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Get the resources based on the community id.

**Arguments**:
  * **id**, the id of the community to explore.
  * **resource_id**, the id of the resource (**optional**).

**Return**::

  [
    {
        "author": {
            "username": "admin"
        }, 
        "tags": "jajaja", 
        "excerpt": "Explicacion de como instalar Maven para Eclipse", 
        "body_html": "En esta entrada vamos a comentar como podemos hacer uso de Maven para Eclipse gracias a un plugin llamado M2E. Gracias a este podemos bajarnos las librerias que nos hagan falta de forma sencilla y rapida.Procedemos con la explicacion:", 
        "community": {
            "title": "LTO"
        }, 
        "title": "Maven para eclipse", 
        "pub_date": "2011-05-11", 
        "id": 1
    }, 
    {
      ...
    }
  ]


**URL**::

  http://localhost:8000/api/community/<id>/resources/

  http://localhost:8000/api/community/<id>/resources/<resource_id>/

**Method** GET

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/1/resources/

^^^^^^^^^^^^^^^^^^^^^^^^^^
Create resource
^^^^^^^^^^^^^^^^^^^^^^^^^^
Create a new resource

**Arguments**:
  * **community**, the id of the community.
  * **title**, the title of the resource.
  * **excerpt**, a brief description.
  * **body**, the content of the resource.
  * **tags**, the tags.
  * **pub_date**, the publication date of the resource (format: YYYY-MM-DD)
  * **type**, where it is a natural number with the following relation::

      1: LIVE, the resource is public
      2: DRAFT, the resource is a draft and therefore, won't be public
      3: HIDDEN, the resource is hidden, which means not public.

**Return**::

  {
    "body": "mas pruebas", 
    "tags": "jaja", 
    "author": {
        "username": "admin"
    }, 
    "excerpt": "nada", 
    "community": {
        "title": "LTO"
    }, 
    "title": "Pruebas", 
    "pub_date": "2011-12-07", 
    "id": 11
  }

**URL**::

  http://localhost:8000/api/community/resource/

**Method** POST

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/resource/' -F 'community=1' -F 'title=Pruebas' -F 'body=mas pruebas' -F 'pub_date=2011-12-07' -F 'type=1' -F 'tags=jaja' -F 'excerpt=nada' -X POST

^^^^^^^^^^^^^^^^^^^^^^^^^^
Update resource
^^^^^^^^^^^^^^^^^^^^^^^^^^
Update the given resource

**Arguments**:
  * **title**, the title of the resource (**optional**).
  * **excerpt**, a brief description (**optional**).
  * **body**, the content of the resource (**optional**).
  * **tags**, the tags (**optional**).
  * **pub_date**, the publication date of the resource (format: YYYY-MM-DD) (**optional**).
  * **type**, (**optional**) where it is a natural number with the following relation::

      1: LIVE, the resource is public
      2: DRAFT, the resource is a draft and therefore, won't be public
      3: HIDDEN, the resource is hidden, which means not public.

**Return**::

  {
    "body": "mas pruebas", 
    "tags": "jaja", 
    "author": {
        "username": "admin"
    }, 
    "excerpt": "nada", 
    "community": {
        "title": "LTO"
    }, 
    "title": "Pruebas", 
    "pub_date": "2011-12-07", 
    "id": 11
  }

**URL**::

  http://localhost:8000/api/community/resource/<id>/

**Method** PUT

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/resource/11/' -F 'title=Pruebas' -X PUT

^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete resource
^^^^^^^^^^^^^^^^^^^^^^^^^^
Delete the given resource

**Arguments**:
  * **id**, the id of the resource.

**Return** True

**URL**::

  http://localhost:8000/api/community/resource/<id>/

**Method** DELETE

**Example**::
  
  curl -u admin:1234 'http://localhost:8000/api/community/resource/11/' -X DELETE