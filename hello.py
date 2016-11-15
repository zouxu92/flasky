# -*- coding:utf-* -*-

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

# 表单
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Required

app = Flask(__name__)
# 设置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string' # 保证安全不应该写入这里,写在配置文件中
bootstrap = Bootstrap(app)
# 初始化flask_moment --> 本地时间
moment = Moment(app)

# 定义表单类
class NameForm(Form):
	name = StringField('What is your name?', validators=[InputRequired()])
	submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():
	# name = None
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		# 判断输入的名字不为空且不等于旧的session名字,(名字更改了),提示用户
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed you name!')
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'),
						   current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500



if __name__ == '__main__':
	app.run(debug=True)
