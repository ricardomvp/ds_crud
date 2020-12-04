# ds_crud
## A technical test

ds_crud is a tool to admin users and teams.

### set enviroment variables
- touch . . /.env

- add to .env
SECRET_KEY=A_SECRET_KEY

EMAIL_HOST_USER=EMAIL_HOST_ACCOUNT

EMAIL_HOST_PASSWORD=EMAIL_HOST_ACCOUNT_PASSWORD

### setup
- docker-compose down
- docker-compose up
- docker-compose run web python manage.py makemigrations
- docker-compose run web python manage.py migrate
- docker-compose run web python manage.py createsuperuser
  _"Add a email and password"_
- docker-compose up

### Management
in http://localhost:8000/admin/ access to django admin to manage Users & Teams

---
#### Users methods
##### Show
- in http://localhost:8000/users/__show_all__  _#"Show all users"_
- in http://localhost:8000/users/__show/<id>__  _#"Show user with the specific id"_
##### Create
- in http://localhost:8000/users/__create/{}__  _#"Create an user users"_
-- _with dict like this structure  
  __{"email":"email@email.com","name":"SamSam","password":"trecetrecedos","is_admin":"False"}___
##### Delete
- in http://localhost:8000/users/__delete/{"name":"SamSam"}__  _#"Delete specific user"_
##### Modify
- in http://localhost:8000/users/__modify/{"name":"SamSam","new_name":"Armando"}__  _#"Modify specific user"_
---
#### Teams methods
##### Show
- in http://localhost:8000/teams/__show_all__  _#"Show all teams"_
- in http://localhost:8000/teams/__show/<id>__  _#"Show team with the specific id"_
##### Create
- in http://localhost:8000/teams/__create/{"name":"NEW_TEAM_NAME"}__  _#"Create a team"_
##### Delete
- in http://localhost:8000/teams/__delete/{"name":"TEAM_2_DELETE"}__  _#"Delete specific team"_
##### Modify
- in http://localhost:8000/teams/__modify/{"name" : "TEAM_2_MODIFY","new_name":"NEW_NAME"}__  _#"Modify specific team"_
- in http://localhost:8000/teams/__add/{"user":"USER_NAME","team":"TEAM_NAME"}__  _#"Add user to team"_
- in http://localhost:8000/teams/__remove/{"user":"USER_NAME","team":"TEAM_NAME"}__  _#"Remove user from team"_
