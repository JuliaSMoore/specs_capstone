import os
from random import choice, randint

import model
import controller
import server

if os.path.exists("./instance/request.db"):
    os.remove("./instance/request.db")

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

for n in range(20):
    username = f'user{n}'
    email = f'user{n}@test.com'
    password = 'test'
    list_of_categories = ['Writer', 'Reader']
    category = choice(list_of_categories)

    user = controller.create_user(username, email, password, category)
    with server.app.app_context():
        model.db.session.add(user)
        model.db.session.commit()

for n in range(20):
    name = f'character{n}'
    description = f'This is a very <b>cool</b> and appealing character {n} that did so <i>many</i> cool things in their life and have more to do! <br> Write about me!'
    user = randint(1, 20)
    character = controller.create_character(name, description, None, user)
    with server.app.app_context():
        model.db.session.add(character)
        model.db.session.commit()

for n in range(20):
    title = f'request{n}'
    description = f"This is a great <b>request</b> {n} I'm submitting and I would <i>like</i> to read a story about something great and awesome. <br> Please, writers, write this story for me!"
    user = randint(1, 20)
    request = controller.create_request(title, description, None, user)
    with server.app.app_context():
        model.db.session.add(request)
        model.db.session.commit()

tag1 = controller.create_tag('Fantasy')
tag2 = controller.create_tag('Sci-Fi')
tag3 = controller.create_tag('Romance')
tag4 = controller.create_tag('Children\'s')
tag5 = controller.create_tag('Mystery')
tag6 = controller.create_tag('Thriller')
tag7 = controller.create_tag('Detective')
tag8 = controller.create_tag('Historical')
tag9 = controller.create_tag('Drama')
tag10 = controller.create_tag('Humor')

with server.app.app_context():
    model.db.session.add_all(
        [tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10])
    model.db.session.commit()


for n in range(30):
    score = randint(1, 5)
    request_id = randint(1, 20)
    user_id = randint(1, 20)

    rating = controller.create_rating(score, request_id, user_id)

    with server.app.app_context():
        model.db.session.add(rating)
        model.db.session.commit()


for n in range(30):
    text = f"This is a comment or a review {n} left for one of those <b>awesome</b> requests. <br>I <i>definitely</i> like this idea and hope somebody is going to write about it!"
    request_id = randint(1, 20)
    user_id = randint(1, 20)

    comment = controller.create_comment(text, request_id, user_id)

    with server.app.app_context():
        model.db.session.add(comment)
        model.db.session.commit()


for n in range(15):
    request_id = randint(1, 20)
    character_id = randint(1, 20)

    request_character = controller.create_request_character(
        request_id, character_id)

    with server.app.app_context():
        model.db.session.add(request_character)
        model.db.session.commit()


for n in range(30):
    request_id = randint(1, 20)
    tag_id = randint(1, 20)

    request_tag = controller.create_request_tag(request_id, tag_id)

    with server.app.app_context():
        model.db.session.add(request_tag)
        model.db.session.commit()
