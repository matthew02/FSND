from datetime import datetime
from flask import Blueprint, redirect, render_template, request, session, url_for

from forms import *
from models.artist import Artist
from models.show import Show
from models.venue import Venue

artist_blueprint = Blueprint(
    'artists',
    __name__,
    template_folder='templates'
)


@artist_blueprint.route('')
def index():
    return render_template(
        'pages/artists.html',
        artists=Artist.query.order_by('name').all()
    )

@artist_blueprint.route('/search', methods=['POST'])
def search():
    query = request.form.get('search_term')
    artists = Artist.query.filter(Artist.name.ilike(f'%{query}%')).all()
    response = {'count': len(artists), 'data': artists,}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_blueprint.route('/<int:artist_id>')
def view(artist_id):
    current_time = datetime.now()
    artist = Artist.query.get(artist_id)
    setattr(artist, 'past_shows', [])
    setattr(artist, 'upcoming_shows', [])

    for show in artist.shows:
        venue = Venue.query.get(show.venue_id)
        show_details = {
            'venue_id': show.venue_id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time,
        }
        if show.start_time < current_time:
            artist.past_shows.append(show_details)
        else:
            artist.upcoming_shows.append(show_details)

    setattr(artist, 'past_shows_count', len(artist.past_shows))
    setattr(artist, 'upcoming_shows_count', len(artist.upcoming_shows))

    return render_template(
        'pages/show_artist.html',
        artist=artist
    )

#  Update
#  ----------------------------------------------------------------
@artist_blueprint.route('/<int:artist_id>/edit', methods=['GET'])
def edit_form(artist_id):
    form = ArtistForm()
    artist={
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@artist_blueprint.route('/<int:artist_id>/edit', methods=['POST'])
def edit(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('artist.view', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@artist_blueprint.route('/create', methods=['GET'])
def create_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@artist_blueprint.route('/create', methods=['POST'])
def create():
    error = False
    venue = Artist(**request.form)

    try:
        artist = Artist(**request.form)
        if artist.seeking_venue == 'y':
            artist.seeking_venue = True
        else:
            artist.seeking_venue = False
        artist.insert()
    except Exception as e:
        error = True
        db.session.rollback()
        print(f'Exception ==> {e}')
    finally:
        db.session.close()

    if error:
        flash(
            f'An error occurred.'
            f'Artist {request.form["name"]} could not be listed.',
            'error'
        )
    else:
        flash(f'Artist {request.form["name"]} was successfully listed!')

    return render_template('pages/home.html')

@artist_blueprint.route('/<artist_id>', methods=['DELETE'])
def delete(artist_id):
    error = False

    try:
        artist = Artist.query.get(artist_id)
        artist.delete()
    except Exception as e:
        error = True
        print(f'Exception ==> {e}')
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash(f'An error occurred.'
              f'Artist {artist_id} could not be deleted.',
              'error')
    else:
        flash(f'Artist {artist_id} was successfully deleted.')

    return redirect(url_for('index'))
