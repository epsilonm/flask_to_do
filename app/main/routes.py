from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import CategoryForm, NoteForm
from app.models import Category, Note, User


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # убрать повторяющийся код
    user = User.query.filter_by(id=current_user.get_id()).first()
    notes = Note.query.filter_by(user_id=user.id, is_done=False).all()
    categories = Category.query.all()
    return render_template(
        'index.html', title='Home', user=user,
        notes=notes, categories=categories)


@bp.route('/archive', methods=['GET'])
def archive():
    user = User.query.filter_by(id=current_user.get_id()).first()
    notes = Note.query.filter_by(user_id=user.id, is_done=True).all()
    categories = Category.query.all()
    return render_template(
        'index.html', title='Archive', user=user, notes=notes,
        categories=categories)


@bp.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template(
        'add_category.html', title='Add category', form=form)


@bp.route('/category/<id>', methods=['GET'])
def category(id):
    categories = Category.query.all()
    user = User.query.filter_by(id=current_user.get_id()).first()
    category = Category.query.filter_by(id=id).first()
    title = category.name
    notes = Note.query.filter_by(
        category=category, user_id=user.id, is_done=False)
    # придумать как отрефакторить повторяющийся запрос
    return render_template(
        'index.html', title=title, notes=notes,
        user=user, categories=categories)


@login_required
@bp.route('/post', methods=['GET', 'POST'])
def post():
    form = NoteForm()
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by('name')]
    if form.validate_on_submit():
        note = Note(
            user_id=current_user.get_id(), header=form.header.data,
            text=form.text.data, expires_on=form.expires_on.data,
            category_id=form.category_id.data)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post.html', title='Добавить запись', form=form)


@bp.route('/delete/<id>', methods=['GET'])
def delete(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/is_done/<id>', methods=['GET', 'POST'])
def is_done(id):
    note = Note.query.filter_by(id=id).first()
    note.is_done = True
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/note/<id>', methods=['GET', 'POST'])
def note(id):
    user = User.query.filter_by(id=current_user.get_id()).first()
    note = Note.query.filter_by(id=id).first()
    return render_template('note.html', title='Note', note=note, user=user)
