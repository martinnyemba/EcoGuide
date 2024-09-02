from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Role, Contact
from app.admin_forms import UserForm, RoleForm, ContactForm
from functools import wraps
from sqlalchemy import desc

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'Admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_contacts = Contact.query.count()
    recent_users = User.query.order_by(desc(User.id)).limit(5).all()
    recent_contacts = Contact.query.order_by(desc(Contact.timestamp)).limit(5).all()
    return render_template('admin/dashboard.html', total_users=total_users, total_contacts=total_contacts,
                           recent_users=recent_users, recent_contacts=recent_contacts)

@bp.route('/admin/users')
@login_required
@admin_required
def list_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/list_users.html', users=users)

@bp.route('/admin/user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/admin/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.list_users'))

@bp.route('/admin/contacts')
@login_required
@admin_required
def list_contacts():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.order_by(desc(Contact.timestamp)).paginate(page=page, per_page=20)
    return render_template('admin/list_contacts.html', contacts=contacts)

@bp.route('/admin/contact/<int:id>')
@login_required
@admin_required
def view_contact(id):
    contact = Contact.query.get_or_404(id)
    return render_template('admin/view_contact.html', contact=contact)

@bp.route('/admin/contact/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact message deleted successfully.', 'success')
    return redirect(url_for('admin.list_contacts'))