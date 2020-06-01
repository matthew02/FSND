from flask import Blueprint, redirect, render_template, request, session, url_for

from forms import *
from models.artist import Artist
from models.show import Show
from models.venue import Venue

venue_blueprint = Blueprint(
    'venues',
    __name__,
    template_folder='templates'
)


@venue_blueprint.route('/')
def index():
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

@venue_blueprint.route('/search', methods=['POST'])
def search():
    query = request.form.get('search_term')
    venues = Venue.query.filter(Venue.name.ilike(f'%{query}%')).all()
    response = {'count': len(venues), 'data': venues,}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venue_blueprint.route('/<int:venue_id>')
def view(venue_id):
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

@venue_blueprint.route('/create', methods=['GET'])
def create_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@venue_blueprint.route('/create', methods=['POST'])
def create():
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

@venue_blueprint.route('/<venue_id>', methods=['DELETE'])
def delete(venue_id):
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

@venue_blueprint.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_form(venue_id):
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

@venue_blueprint.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))
