from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from model import connect_to_db, db
from forms import RequestForm, CharacterForm, CommentForm, RatingForm, LoginForm, RegisterForm, AddTagsForm, AddCharactersForm
import controller
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return controller.get_user_by_id(user_id)


# HOME

@app.route('/')
def home():
    return render_template('home.html')

# REQUEST


@app.route('/requests')
def requests():
    requests = controller.get_all_requests()
    return render_template('requests.html', requests=requests)


@app.route('/requests/<request_id>')
@login_required
def request(request_id):
    rating_form = RatingForm()
    comment_form = CommentForm()
    tag_form = AddTagsForm()
    character_form = AddCharactersForm()
    request = controller.get_request(request_id)
    comments = controller.get_comments(request_id)
    tags = controller.get_tags_by_request_id(request_id)
    characters = controller.get_characters_by_request_id(request_id)
    ratings_average = controller.avg_rating_by_request_id(request_id)[0]
    ratings_total = controller.get_total_ratings_bt_request_id(request_id)
    rating = controller.get_rating_by_request_id_and_user_id(
        request_id, current_user.id)
    return render_template('request.html', request=request, comment_form=comment_form, comments=comments, tags=tags, characters=characters, ratings_total=ratings_total, ratings_average=ratings_average, rating_form=rating_form, rating=rating, tag_form=tag_form, character_form=character_form)


@app.route('/create_request')
@login_required
def create_request():
    request_form = RequestForm()
    return render_template('create-request.html', request_form=request_form)


@app.route('/requests', methods=["POST"])
def add_request():
    request_form = RequestForm()

    if request_form.validate_on_submit():
        title = request_form.title.data
        description = request_form.description.data
        image_url = request_form.image_url.data
        created_by_id = current_user.id
        new_request = controller.create_request(
            title, description, image_url, created_by_id)
        db.session.add(new_request)
        db.session.commit()
        new_request2 = controller.get_request(new_request.request_id)
        request_id = new_request2.request_id
        return redirect(f'/requests/{request_id}')


@app.route('/delete_request/<request_id>')
def delete_request(request_id):
    request_character = controller.get_request_character_req(request_id)
    request_tag = controller.get_request_tag(request_id)
    comment = controller.get_comment_by_request_id(request_id)
    rating = controller.get_rating_by_request_id(request_id)
    request = controller.get_request(request_id)
    for req_id in request_character:
        db.session.delete(req_id)
    for req_id in request_tag:
        db.session.delete(req_id)
    for req_id in comment:
        db.session.delete(req_id)
    for req_id in rating:
        db.session.delete(req_id)
    db.session.delete(request)
    db.session.commit()
    return redirect('/requests')


@app.route('/book_request/<request_id>')
def book_request(request_id):
    request = controller.get_request(request_id)
    request.booked = True
    request.status = "In Process"
    request.booked_by_id = current_user.id
    db.session.add(request)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


@app.route('/complete_request/<request_id>')
def complete_request(request_id):
    request = controller.get_request(request_id)
    request.status = "Complete"
    db.session.add(request)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


@app.route('/drop_request/<request_id>')
def drop_request(request_id):
    request = controller.get_request(request_id)
    request.booked = False
    request.status = "Avaliable"
    request.booked_by_id = None
    db.session.add(request)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


# CHARACTER

@app.route('/characters')
def characters():
    characters = controller.get_all_characters()
    return render_template('characters.html', characters=characters)


@app.route('/characters/<character_id>')
@login_required
def character(character_id):
    character = controller.get_character(character_id)
    return render_template('/character.html', character=character)


@app.route('/create_character')
def create_character():
    character_form = CharacterForm()
    return render_template('create-character.html', character_form=character_form)


@app.route('/characters', methods=["POST"])
@login_required
def add_character():
    character_form = CharacterForm()

    if character_form.validate_on_submit():
        name = character_form.name.data
        description = character_form.description.data
        image_url = character_form.image_url.data
        created_by_id = current_user.id
        new_character = controller.create_character(
            name, description, image_url, created_by_id)
        db.session.add(new_character)
        db.session.commit()
        new_character2 = controller.get_character(new_character.character_id)
        character_id = new_character2.character_id
        return redirect(f'/characters/{character_id}')


@app.route('/delete_character/<character_id>')
def delete_character(character_id):
    request_character = controller.get_request_character_char(character_id)
    for char_id in request_character:
        db.session.delete(char_id)
    character = controller.get_character(character_id)
    db.session.delete(character)
    db.session.commit()
    return redirect('/characters')


@app.route('/book_character/<character_id>')
def book_character(character_id):
    character = controller.get_character(character_id)
    character.booked = True
    character.status = "In Process"
    character.booked_by_id = current_user.id
    db.session.add(character)
    db.session.commit()
    return redirect(f'/characters/{character_id}')


@app.route('/complete_character/<character_id>')
def complete_character(character_id):
    character = controller.get_character(character_id)
    character.status = "Complete"
    db.session.add(character)
    db.session.commit()
    return redirect(f'/characters/{character_id}')


@app.route('/drop_character/<character_id>')
def drop_character(character_id):
    character = controller.get_character(character_id)
    character.booked = False
    character.status = "Avaliable"
    character.booked_by_id = None
    db.session.add(character)
    db.session.commit()
    return redirect(f'/characters/{character_id}')

@app.route('/<request_id>/add_character_to_request/', methods=["POST"])
def add_character_to_request(request_id):
    character_form = AddCharactersForm()
    characters = character_form.characters.data
    print(characters)
    for character in characters:
        print(character)
        character_id = controller.get_character_by_name(character)
        print(character_id)
        print(character_id.character_id)
        entry = controller.create_request_character(request_id, character_id.character_id)
        db.session.add(entry)
        db.session.commit()
    return redirect(f'/requests/{request_id}')

@app.route('/delete_character_from_request/<request_id>/<character_id>')
def delete_character_from_request(request_id, character_id):
    character = controller.get_character_by_both_ids(request_id, character_id)
    db.session.delete(character)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


# COMMENT

@app.route('/<request_id>/add_comment', methods=["POST"])
def add_comment(request_id):
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        text = comment_form.text.data
        user_id = current_user.id
        new_comment = controller.create_comment(text, request_id, user_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(f'/requests/{request_id}')


@app.route('/edit_comment/<comment_id>', methods=["GET", "POST"])
def edit_comment(comment_id):
    comment = controller.get_comment_by_id(comment_id)
    comment_form = CommentForm(obj=comment)
    if comment_form.validate_on_submit():
        comment.text = comment_form.text.data
        db.session.add(comment)
        db.session.commit()
        return redirect(f'/requests/{comment.request_id}')
    return render_template('edit-comment.html', comment_form=comment_form, comment=comment)


@app.route('/delete_comment/<request_id>/<comment_id>')
def delete_comment(request_id, comment_id):
    comment = controller.get_comment_by_id(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


# RATING

@app.route('/<request_id>/rate_request', methods=["POST"])
def rate_request(request_id):
    rating_form = RatingForm()

    if rating_form.validate_on_submit():
        score = rating_form.score.data
        user_id = current_user.id
        new_rating = controller.create_rating(score, request_id, user_id)
        db.session.add(new_rating)
        db.session.commit()
        return redirect(f'/requests/{request_id}')


@app.route('/edit_rating/<rating_id>', methods=["GET", "POST"])
def edit_rating(rating_id):
    rating = controller.get_rating_by_id(rating_id)
    rating_form = RatingForm(obj=rating)

    if rating_form.validate_on_submit():
        rating.score = rating_form.score.data
        db.session.add(rating)
        db.session.commit()
        return redirect(f'/requests/{rating.requests.request_id}')
    return render_template('edit-rating.html', rating=rating, rating_form=rating_form)


#TAGS

@app.route('/<request_id>/add_tags', methods=["GET", "POST"])
def add_tags(request_id):
    tag_form = AddTagsForm()
    tags = tag_form.tags.data
    for tag in tags:
        tag_id = controller.get_tags_by_name(tag)
        entry = controller.create_request_tag(request_id, tag_id.tag_id)
        db.session.add(entry)
        db.session.commit()
    return redirect(f'/requests/{request_id}')

@app.route('/delete_tag/<request_id>/<tag_id>')
def delete_tag(request_id, tag_id):
    tag = controller.get_request_tag_by_both_ids(request_id, tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/requests/{request_id}')


# @app.route('/try_code')
# def try_code():
#     tag_form = AddTagsForm()
#     return render_template('try-code.html', tag_form=tag_form)


# LOGIN


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = controller.get_user_by_email(email)
        if user.check_password(password) and user:
            login_user(user)
            flash('Logged in!')
            # next = request.args.get('next')
            # if next == None:
            #     next = url_for('requests')
            # return redirect(next)
            return redirect(url_for('requests'))
    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        category = register_form.category.data

        user = controller.create_user(username, email, password, category)
        db.session.add(user)
        db.session.commit()
        flash('You are registered!')
        return redirect(url_for('login'))
    return render_template('register.html', register_form=register_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('login'))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
