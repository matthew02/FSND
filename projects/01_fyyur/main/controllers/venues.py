from app import app
from models.artist import Artist
from models.show import Show
from models.venue import Venue


@app.route('/venues')
def venues():
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
