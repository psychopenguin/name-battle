#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
from flask.ext.stormpath import StormpathManager, login_required, user
from dbfunctions import ranking, getbattle, dobattle, isparent
from config import application


app = Flask(__name__)
app.config['SECRET_KEY'] = application['secret_key']
app.config['STORMPATH_API_KEY_FILE'] = application['stormpath']['api_key_file']
app.config['STORMPATH_APPLICATION'] = 'Flask Test'
app.config['STORMPATH_ENABLE_FACEBOOK'] = True
app.config['STORMPATH_SOCIAL'] = {
    'FACEBOOK': {
        'app_id': '<FB_APP_ID>',
        'app_secret': '<SECRET>',
    }
}
app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'

stormpath_manager = StormpathManager(app)


@app.route('/')
@login_required
def home():
    if isparent(user.email):
        return render_template('battle.html',
                               user=user,
                               ranking=ranking(),
                               battle=getbattle(user.email))
    else:
        return render_template('parents-only.html',
                               user=user,
                               ranking=ranking())


@app.route('/battle/<home>-<visitor>-<int:winner>')
@login_required
def battle(home, visitor, winner):
    dobattle((home, visitor), user.email, winner)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
