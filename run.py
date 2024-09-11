#!/usr/bin/env python
"""Module to run the application as Entry Point"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
