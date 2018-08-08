from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import User
from flask import jsonify, request, url_for
from app.api.auth import token_auth


def get_per_page():
    return min(request.args.get('per_page', 10, type=int), 100)


def get_page():
    return request.args.get('page', 1, type=int)


@bp.route('/user/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = get_page()
    per_page = get_per_page()
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    data = User.to_collection_dict(
        query=User.query.get_or_404(id).followers,
        page=get_page(),
        per_page=get_per_page(),
        endpoint='api.get_followers',
        id=id
    )
    return jsonify(data)


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    data = User.to_collection_dict(
        query=User.query.get_or_404(id).followed,
        page=get_page(),
        per_page=get_per_page(),
        endpoint='api.get_followed',
        id=id
    )
    return jsonify(data)


@bp.route('/users', methods=['POST'])
@token_auth.login_required
def create_user():
    data = request.get_json() or {}

    if 'username' not in data or 'email' not in data or 'password' not in data:
       return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
       return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
       return bad_request('please use a different email')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    def update_is_collading_with_other_user(user, request_data):
        return ('username' in request_data and request_data['username'] != user.username and
                User.query.filter_by(username=request_data['username']).first()) \
               or \
               ('email' in request_data and request_data['email'] != user.email and
                User.query.filter_by(email=request_data['email']).first())

    user = User.query.get_or_404(id)
    data = request.get_json() or {}

    if update_is_collading_with_other_user(user, data):
        bad_request("can't use that username or email")
    else:
        user.from_dict(data, new_user=False)
        db.session.commit()
        return jsonify(user.to_dict())
