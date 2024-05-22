import flask_login

users = {
"user1":"1234",
"user2":"12345"
}

adm ={"adm": "adm1"}
    


class User(flask_login.UserMixin):
    def get_adm():
        global adm
        return adm

    def get_users():
        global users
        return users

    def add_user(user, password):
        users[user] = password
        return users

    def remove_user(user):
        users.pop(user)
        return users

