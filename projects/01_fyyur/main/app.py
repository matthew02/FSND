#!/usr/bin/env python3

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import babel
import datetime
import dateutil.parser
import json
import logging

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from logging import Formatter, FileHandler
#from sqlalchemy.ext.declarative import as_declarative

from forms import *
from models.model import db, Model
from models.venue import Venue
from models.artist import Artist
from models.show import Show


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if not value:
        return "TBA"
    else:
        return value.strftime('%A %B %-d, %Y at %-I:%M %p')
    #date = dateutil.parser.parse(value)
    #if format == 'full':
    #    format="EEEE MMMM, d, y 'at' h:mma"
    #elif format == 'medium':
    #    format="EE MM, dd, y h:mma"

    #return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: Sort by state and city
    venues = Venue.query.all()
    locations = set((venue.city, venue.state) for venue in venues)
    areas = [
        {
            'city': location[0],
            'state': location[1],
            'venues': Venue.query
                           .filter(Venue.city == location[0])
                           .filter(Venue.state == location[1])
                           .all()
        }
        for location
        in locations
    ]
    return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    query = request.form.get('search_term')
    venues = Venue.query.filter(Venue.name.ilike(f'%{query}%')).all()
    response = {'count': len(venues), 'data': venues,}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    current_time = datetime.now()
    venue = Venue.query.get(venue_id)
    setattr(venue, 'past_shows', [])
    setattr(venue, 'upcoming_shows', [])

    for show in venue.shows:
        artist = Artist.query.get(show.artist_id)
        show_details = {
            'artist_id': show.artist_id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time,
        }
        if show.start_time < current_time:
            venue.past_shows.append(show_details)
        else:
            venue.upcoming_shows.append(show_details)

    setattr(venue, 'past_shows_count', len(venue.past_shows))
    setattr(venue, 'upcoming_shows_count', len(venue.upcoming_shows))

    return render_template(
        'pages/show_venue.html',
        venue=Venue.query.get(venue_id)
    )

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    venue = Venue(**request.form)

    try:
        venue = Venue(**request.form)
        if venue.seeking_talent == 'y':
            venue.seeking_talent = True
        else:
            venue.seeking_talent = False
        venue.insert()
    except Exception as e:
        error = True
        db.session.rollback()
        print(f'Exception ==> {e}')
    finally:
        db.session.close()

    if error:
        flash(
            f'An error occurred.'
            f'Venue {request.form["name"]} could not be listed.',
            'error'
        )
    else:
        flash(f'Venue {request.form["name"]} was successfully listed!')

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False

    try:
        venue = Venue.query.get(venue_id)
        venue.delete()
    except Exception as e:
        error = True
        print(f'Exception ==> {e}')
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash(f'An error occurred.'
              f'Venue {venue_id} could not be deleted.',
              'error')
    else:
        flash(f'Venue {venue_id} was successfully deleted.')

    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template(
        'pages/artists.html',
        artists=Artist.query.order_by('name').all()
    )

@app.route('/artists/search', methods=['POST'])
def search_artists():
    query = request.form.get('search_term')
    artists = Artist.query.filter(Artist.name.ilike(f'%{query}%')).all()
    response = {'count': len(artists), 'data': artists,}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
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
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
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

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue={
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
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

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
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


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    for show in shows:
        show.venue_name = Venue.query.get(show.venue_id).name
        artist = Artist.query.get(show.artist_id)
        show.artist_name = artist.name
        show.artist_image_link = artist.image_link

    return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
