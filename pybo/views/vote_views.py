from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Article, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/article/<int:article_id>/')
@login_required
def article(article_id):
    _article = Article.query.get_or_404(article_id)
    if g.user == _article.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _article.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('article.detail', article_id=article_id))

@bp.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('article.detail', article_id=_answer.article.id))