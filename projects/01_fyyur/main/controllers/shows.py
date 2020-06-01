from flask import Blueprint, redirect, render_template, request, session, url_for

from forms import *
from models.artist import Artist
from models.show import Show
from models.venue import Venue

show_blueprint = Blueprint(
    'shows',
    __name__,
    template_folder='templates'
)


@show_blueprint.route('')
def index():
    shows = Show.query.all()
    for show in shows:
        show.venue_name = Venue.query.get(show.venue_id).name
        artist = Artist.query.get(show.artist_id)
        show.artist_name = artist.name
        show.artist_image_link = artist.image_link

    return render_template('pages/shows.html', shows=shows)

@show_blueprint.route('/create')
def create_form():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@show_blueprint.route('/create', methods=['POST'])
def create():
    error = False

    data = request.form.to_dict()
    format = '%Y-%m-%d %H:%M:%S'
    data['start_time'] = datetime.strptime(data['start_time'], format)

    try:
        show = Show(**data)
        show.insert()
    except Exception as e:
        error = True
        db.session.rollback()
        print(f'Exception ==> {e}')
    finally:
        db.session.close()

    if error:
        flash('An error occurred and the show could not be listed.', 'error')
    else:
        flash('The show was successfully listed.')

    return render_template('pages/home.html')

