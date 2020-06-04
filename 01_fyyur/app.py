#!/usr/bin/env python3

import datetime
import logging

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_moment import Moment
from logging import Formatter, FileHandler


from controllers.artists import artist_blueprint
from controllers.shows import show_blueprint
from controllers.venues import venue_blueprint
from models.model import db


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

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
# Register controller blueprints.
#----------------------------------------------------------------------------#
app.register_blueprint(artist_blueprint, url_prefix='/artists')
app.register_blueprint(show_blueprint, url_prefix='/shows')
app.register_blueprint(venue_blueprint, url_prefix='/venues')


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
    if not value:
        return "TBA"
    else:
        return value.strftime('%A %B %-d, %Y at %-I:%M %p')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
