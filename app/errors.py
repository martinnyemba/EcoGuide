# from flask import render_template
# import app
#
#
# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('errors/404.html'), 404
#
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('errors/500.html'), 500
#
# @app.errorhandler(403)
# def forbidden_error(error):
#     return render_template('errors/403.html'), 403
#
# @app.errorhandler(Exception)
# def unhandled_exception(e):
#     app.logger.error('Unhandled Exception: %s', (e))
#     return render_template('errors/500.html'), 500