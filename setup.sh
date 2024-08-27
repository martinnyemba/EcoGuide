#!/bin/bash

# Create the main directory structure
mkdir -p app/{routes,static/{css,js},templates/{auth,user,admin}}

# Create the Python files in the 'app' directory
touch app/__init__.py app/models.py app/forms.py app/utils.py

# Create the Python files in the 'routes' directory
touch app/routes/{__init__.py,main.py,auth.py,user.py,admin.py}

# Create the HTML files in the 'templates' directory
touch app/templates/{base.html,index.html}

# Create the auth, user, and admin directories under templates with no files
# (these directories will be empty initially)

# Create the root-level files
touch config.py requirements.txt run.py

echo "Directory structure and files created successfully."
