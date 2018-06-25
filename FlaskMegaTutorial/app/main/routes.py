from app import db
from app.main.forms import EditProfileForm
from app.main.forms import PostForm
from app.main import bp
from app.models import Post
from app.models import User
from app.translate import translate
from flask import current_app
from flask import flash
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_babel import _
from flask_babel import get_locale
from flask_login import current_user
from flask_login import login_required
from guess_language import guess_language
from flask import g
from app.main.forms import SearchForm

URL_NAMES = {
    'index': 'main.index',
    'user': 'main.user',
    'register': 'main.register',
    'explore': 'main.explore'
}

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_last_seen()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for(URL_NAMES['index']))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for(URL_NAMES['index'], page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for(URL_NAMES['index'], page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Home'),
                           posts=posts.items, form=form,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for(URL_NAMES['user'], username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for(URL_NAMES['user'], username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.update_profile(form.username.data, form.about_me.data)
        flash(_('Your changes have been saved.'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found', username=username))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for(URL_NAMES['user'], username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for(URL_NAMES['user'], username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for(URL_NAMES['index']))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for(URL_NAMES['user'], username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('Your are not following %(username)s', username=username))
    return redirect(url_for(URL_NAMES['user'], username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query. \
        order_by(Post.timestamp.desc()). \
        paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for(URL_NAMES['explore'], page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for(URL_NAMES['explore'], page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Explore'), posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({
        'text': translate(
            request.form['text'],
            request.form['source_language'],
            request.form['dest_language']
        )
    })

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)

    posts, total = Post.search(
        g.search_form.q.data,
        page,
        current_app.config['POSTS_PER_PAGE']
    )

    is_last_page = total <= page * current_app.config['POSTS_PER_PAGE']
    next_url = url_for(
        'main.search',
        q=g.search_form.q.data,
        page=page + 1
    ) if not is_last_page else None

    prev_url = url_for(
        'main.search',
        q=g.search_form.q.data,
        page=page - 1
    ) if page > 1 else None

    return render_template(
        'search.html',
        title=_('Search'),
        posts=posts,
        next_url=next_url,
        prev_url=prev_url
    )
