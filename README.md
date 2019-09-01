# Nasaq-task

Simple state-pattern implmentiotion applied on the case of a Todo App API service.


### An API Documentation of somesort:

**API endpoints & actions**
- create: `POST` - `api/v1/tasks/`
  * request body: {"title": <task-title>, "description": <task-description>}

- list: `GET` `api/v1/tasks/` list all available tasks [doesn't provide filtration yet].

- retrive: `GET` - `api/v1/tasks/{pk}/` retrive a single task data with it's `pk`.

- update: `PATCH` - `api/v1/tasks/{pk}/` update the title or description of a task if it was in a `NEW` state.

- link: `POST` - `api/v1/tasks/{pk}/link/` link a task to another one if the parent task was in an `IN-PROGRESS` state.
  * request body: {'child': <child-task-id>}

- change-state: `POST` - `api/v1/tasks/{pk}/change_state/` froward change the state of a task.


### Clonning & Running the project:
- First thing obviously clone the repo locally.
```
$ git clone git@github.com:mxahmed/nasaq.git
```

- Create a virtual envirnoment for the project the standard `venv` module is prefered.

- Install all needed requirements from requirements.txt
```
$ pip install -r requirements.txt
```

- create a `.env` file that will hold project's envrinoment variables based on `env.example` or directly export the variables in your shell before running any further command.
 
- Apply project migrations, and note that this project uses the default sqlite database setup generated by django.
```
$ ./manange.py migrate
```

- Run the project's test, only test for the todo app are available.
```
$ ./manage.py test todo.tests
```

- And run the project with the development server.
```
$ ./manage.py runserver
```
