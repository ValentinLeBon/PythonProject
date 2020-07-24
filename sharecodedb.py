#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect

from model_sqlite import save, \
    read, \
    getAll

app = Flask(__name__)


@app.route('/')
def index():
    # d = { 'last_added':[ { 'uid':'testuid', 'code':'testcode' } ] }
    choosing = {'py': 'Python', 'c': 'C', 'php': 'PHP', 'js': 'Javascript', 'ja' : 'Java'}
    d = {'last_added': getAll(), 'choosing': choosing}
    return render_template('index.html', **d)


@app.route('/create')
def create():
    language = ''
    if request.args.get('language'):
        language = request.args.get('language')
    uid = save(None, None, language)
    return redirect("{}edit/{}".format(request.host_url, uid))


@app.route('/edit/<string:uid>/')
def edit(uid):
    data = read(uid)
    if data['code'] is None:
        return render_template('error.html', uid=uid)
    choosing = {'python': 'Python', 'c': 'C', 'php': 'PHP', 'javascript': 'Javascript'}
    d = dict(uid=uid, code=data['code'], language=data['language'], choosing=choosing,
            url="{}view/{}".format(request.host_url, uid))
    return render_template('edit.html', **d)


@app.route('/publish', methods=['POST'])
def publish():
    code = request.form['code']
    uid = request.form['uid']
    language = request.form['language']
    save(uid, code, language)
    return redirect("{}{}/{}".format(request.host_url,
                                    request.form['submit'],
                                    uid))


@app.route('/view/<string:uid>/')
def view(uid):
    data = read(uid)
    if data['code'] is None:
        return render_template('error.html', uid=uid)
    d = dict(uid=uid, code=data['code'], language=data['language'],
            url="{}view/{}".format(request.host_url, uid))
    return render_template('view.html', **d)


@app.route('/admin/')
def admin():
    pass


if __name__ == '__main__':
    app.run()