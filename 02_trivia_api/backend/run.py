#!/usr/bin/env python3

from api.app import create_application


if __name__ == '__main__':
    app = create_application('Development')
    app.run()
