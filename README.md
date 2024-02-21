# notes-app

## run this to intsall requirements in not installed previously
 pip install - r requirements

## run this line  to start the flask server on local host
 python app.py

## about the files and flow
app.py file has flask code, api endpoints.

test.ipynb file has some example requests to test the endpoints.

have used free mongo atlas to setup db so you can also test the code in working condition.

notes_app is the db name, it has 4 collections notes, users notes_history and user_notes_map.

app.py has comments in endpoints to explain what the codes does 

## API Reference

#### signup endpoint
```http
  POST /signup
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Name |
| `email` | `string` | **Required**. Email |
| `password` | `string` | **Required**. Password |

``` example response {"message":"Username or email already exists"}```

#### login endpoint
```http
  POST /login
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required**. Email |
| `password`      | `string` | **Required**. Password |

```example response {"message":"Login successful","token":"token_string"}```

#### create new note 
```http
  POST /notes/create
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. Title |
| `content`      | `string` | **Required**. Content |

| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

```example response {"message":"Note created successfully","note_id":"65d4f950a4b7ca8d7c830e3f"}```

### update note
```http
  PUT /notes/${id}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. New Title |
| `content`      | `string` | **Required**. New Content |

| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

```example response {"message":"Note updated successfully"}```

### get note endpoint
```http
  GET /notes/${id}
```
| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

```example response {"content":"biscut are sweet, it is important","title":"note biscuts"}```

### share note to other user
```http
  POST /notes/share
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `note_id`      | `string` | **Required**. note_id to be shared |
| `user_ids`      | `list` | **Required**. user_ids to be assign  |

| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

```example response {"message":"Note shared successfully","note_id":"65d4f950a4b7ca8d7c830e3f","user_ids":"['65d4946c809e8192877a32d5']"}```

### notes version history endpoint
```http
  GET /notes/version-history/${id}
```
| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

```example response [{"modified_at":"2024-02-20 20:15:11.240000","modified_by":"65d490bf809e8192877a32d4","note":"{'title': 'test note', 'content': 'note data is nice', '_id': ObjectId('65d4baf7e0b3db9cc0614149')}","note_id":"65d4baf7e0b3db9cc0614149","version":"1"},{"modified_at":"2024-02-20 20:33:33.921000","modified_by":"65d490bf809e8192877a32d4","note":"{'title': 'updated note 3', 'content': 'notes has updated data'}","note_id":"65d4baf7e0b3db9cc0614149","version":"2"},{"modified_at":"2024-02-21 00:42:32.126000","modified_by":"65d490bf809e8192877a32d4","note":"{'title': 'update biscut', 'content': 'notes has updated data'}","note_id":"65d4baf7e0b3db9cc0614149","version":"3"}]```
