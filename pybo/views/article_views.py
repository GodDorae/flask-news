from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from sqlalchemy import func
from werkzeug.utils import redirect

from .. import db
from ..models import Article, Answer, User, article_voter
from ..forms import ArticleForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(article_voter.c.article_id, func.count('*').label('num_voter')) \
            .group_by(article_voter.c.article_id).subquery()
        article_list = Article.query \
            .outerjoin(sub_query, Article.id == sub_query.c.article_id) \
            .order_by(sub_query.c.num_voter.desc(), Article.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.article_id, func.count('*').label('num_answer')) \
            .group_by(Answer.article_id).subquery()
        article_list = Article.query \
            .outerjoin(sub_query, Article.id == sub_query.c.article_id) \
            .order_by(sub_query.c.num_answer.desc(), Article.create_date.desc())
    else:  # recent
        article_list = Article.query.order_by(Article.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.article_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        article_list = article_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.article_id == Article.id) \
            .filter(Article.subject.ilike(search) |  # 질문제목
                    Article.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    article_list = article_list.paginate(page, per_page=10)
    return render_template('article/article_list.html', article_list=article_list, page=page, kw=kw, so=so)



@bp.route('/detail/<int:article_id>/')
def detail(article_id):
    form = AnswerForm()
    article = Article.query.get_or_404(article_id)
    return render_template('article/article_detail.html', article=article, form=form) 

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        article = Article(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article._list'))
    return render_template('article/article_form.html', form=form)

@bp.route('/modify/<int:article_id>', methods=('GET', 'POST'))
@login_required
def modify(article_id):
    article = Article.query.get_or_404(article_id)
    if g.user != article.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('article.detail', article_id=article_id))
    if request.method == 'POST':  # POST 요청
        form = ArticleForm()
        if form.validate_on_submit():
            form.populate_obj(article)
            article.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('article.detail', article_id=article_id))
    else:  # GET 요청
        form = ArticleForm(obj=article)
    return render_template('article/article_form.html', form=form)

@bp.route('/delete/<int:article_id>')
@login_required
def delete(article_id):
    article = Article.query.get_or_404(article_id)
    if g.user != article.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('article.detail', article_id=article_id))
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('article._list'))