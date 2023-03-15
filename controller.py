from model import User, Character, Request, Tag, Rating, Comment, connect_to_db, Request_Character, Request_Tag, db
from flask import request

# USER


def create_user(username, email, password, category):

    user = User(username=username, email=email,
                password=password, category=category)

    return user


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# CHARACTER

def create_character(name, description, image_url, created_by_id):

    character = Character(name=name, description=description,
                          image_url=image_url, created_by_id=created_by_id)

    return character


def get_all_characters():
    page = request.args.get('page', 1, type=int)
    return Character.query.paginate(page=page, per_page=10)


def get_character(character_id):
    return Character.query.get(character_id)


def get_characters_by_request_id(request_id):
    return Character.query.join(Request_Character).join(Request).filter(Request_Character.request_id == request_id).all()


def get_request_character_char(character_id):
    return Request_Character.query.filter_by(character_id=character_id).all()

def get_characters_by_created_id(created_by_id):
    return Character.query.filter_by(created_by_id=created_by_id).all()

def get_character_by_name(name):
    return Character.query.filter_by(name=name).first()

def get_character_by_both_ids(request_id, character_id):
    return Request_Character.query.filter(Request_Character.request_id == request_id, Request_Character.character_id == character_id).first()


# REQUEST

def create_request(title, description, image_url, created_by_id):

    request = Request(title=title, description=description,
                      image_url=image_url, created_by_id=created_by_id)

    return request


def get_all_requests():
    page = request.args.get('page', 1, type=int)
    return Request.query.paginate(page=page, per_page=10)


def get_request(request_id):
    return Request.query.get(request_id)


def get_request_character_req(request_id):
    return Request_Character.query.filter_by(request_id=request_id).all()


def get_request_tag(request_id):
    return Request_Tag.query.filter_by(request_id=request_id)


# TAG

def create_tag(name):

    tag = Tag(name=name)

    return tag


def get_tags_by_request_id(request_id):
    return Tag.query.join(Request_Tag).join(Request).filter((Request_Tag.request_id == request_id)).all()


def get_tags():
    return Tag.query.all()

def get_tags_by_name(name):
    return Tag.query.filter_by(name=name).first()

def get_request_tag_by_both_ids(request_id, tag_id):
    return Request_Tag.query.filter(Request_Tag.request_id == request_id, Request_Tag.tag_id == tag_id ).first()

# RATING

def create_rating(score, request_id, user_id):

    rating = Rating(score=score, request_id=request_id, user_id=user_id)

    return rating


def get_rating_by_request_id(request_id):
    return Rating.query.filter_by(request_id=request_id)


def get_rating_by_request_id_and_user_id(request_id, user_id):
    return Rating.query.filter(Rating.request_id == request_id, Rating.user_id == user_id).first()


def get_total_ratings_bt_request_id(request_id):
    return Rating.query.filter_by(request_id=request_id).count()


def avg_rating_by_request_id(request_id):
    return db.session.query(db.func.round(db.func.avg(Rating.score), 2)).filter_by(request_id=request_id).first()


def get_rating_by_id(rating_id):
    return Rating.query.get(rating_id)


# COMMENT

def create_comment(text, request_id, user_id):

    comment = Comment(text=text, request_id=request_id, user_id=user_id)

    return comment


def get_comment_by_request_id(request_id):
    return Comment.query.filter_by(request_id=request_id)

def get_comments(request_id):
    page = request.args.get('page', 1, type=int)
    return Comment.query.filter_by(request_id=request_id).paginate(page=page, per_page=10)


def get_comment_by_id(comment_id):
    return Comment.query.get(comment_id)


# MISC

def create_request_character(request_id, character_id):

    request_character = Request_Character(
        request_id=request_id, character_id=character_id)

    return request_character


def create_request_tag(request_id, tag_id):

    request_tag = Request_Tag(request_id=request_id, tag_id=tag_id)

    return request_tag


