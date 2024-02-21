# notes-app

## run this to intsall requirements in not installed previously
```bash
 pip install - r requirements
```

## run this line  to start the flask server on local host
``` bash 
 python app.py
```
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

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `user_id` | `string` | user_id if successful |
| `errors` | `string` | error description |

#### login endpoint
```http
  POST /login
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required**. Email |
| `password`      | `string` | **Required**. Password |

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `token` | `string` | token generated |
| `errors` | `string` | error description |

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

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `note_id` | `string` | note_id generated |
| `errors` | `string` | error description |

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

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `errors` | `string` | error description |

### get note endpoint
```http
  GET /notes/${id}
```
| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `title` | `string` | note title |
| `content` | `string` | note content |


### share note to other user
```http
  POST /notes/share
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `note_id` | `string` | **Required**. note_id to be shared |
| `user_ids` | `list` | **Required**. user_ids to be assign  |

| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `errors` | `string` | error description |
| `note_id` | `string` | note_id generated |
| `user_ids` | `list` | list of user_ids |

### notes version history endpoint
```http
  GET /notes/version-history/${id}
```
| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`| `Bearer token` | **Required**. Token from login |

response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Error or Confirmation message |
| `modified_at` | `string` | last modified timestamp |
| `modified_by` | `string` | user_id of user who modified |
| `note` | `dict` | note description |
| `note_id` | `string` | note_id |
| `version` | `int` | note version |
