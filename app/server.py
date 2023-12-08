import flask
from flask import request
from flask import views, jsonify
from models import Session, User
from sqlalchemy.exc import IntegrityError
from  errors import HttpError
from schema import CreateUser, UpdateUser
from tools import validate
from flask_bcrypt import Bcrypt


print(5+6)
app = flask.Flask("app")
bcrypt = Bcrypt(app)

def hash_password(password: str):
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)

# def hello_world():
#     json_data = request.json
#     query_params = request.args
#     headers = request.headers
#     print(f'{json_data=}')
#     print(f'{query_params=}')
#     print(f'{headers=}')
#
#     http_response = flask.jsonify({'hello': "world"})
#     return http_response

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError( 409, 'user alrady exists')



class UserView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id: int):

        user = get_user(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate(CreateUser, request.json)
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        add_user(user)
        return jsonify({"id": user.id})

    def patch(self, user_id: int):
        user = get_user(user_id)
        user_data = validate(CreateUser, request.json)
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        for key, value in user_data.items():
            setattr(user, key, value)
            add_user(user)
        return jsonify({"id": user.id})

    def delete(self, user_id: int):
        user = get_user(user_id)
        self.session.delete(user)
        return jsonify({"status": "ok"})


user_view = UserView.as_view("user_view")

# app.add_url_rule("/hello/world", view_func=hello_world, methods=['GET', 'POST'])
app.add_url_rule("/users/<int:user_id>", view_func=user_view,
                 methods=['GET', "PATCH", "DELETE"])
app.add_url_rule("/users", view_func=user_view, methods=['POST'])



if __name__ == '__main__':
    app.run()







