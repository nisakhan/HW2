## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed
#inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this
#Flask application code below so that the routes described
#in the README exist and render the templates they are supposed
#to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates
#(new .html files) to the templates directory.

## FOR PROFESSOR: I helped and worked with Sindhu Giri in this homework.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album:', validators=[Required() ])
    num1 = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')])
    submit = SubmitField('Submit')

@app.route('/album_entry')
def album_entry():
  form_var = AlbumEntryForm()
  return render_template('album_entry.html',form=form_var)

@app.route('/album_data', methods=["POST"])
def album_result():
  form = AlbumEntryForm()
  if form.validate_on_submit():
      album = form.album.data
      num = form.num1.data
      return render_template('album_data.html', name=album, number=num)
  return "Sorry, no data available."

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform', methods=["GET"])
def hello_form():
    return render_template('artistform.html')

@app.route('/artistinfo', methods=["GET"])
def hello_artist():
    if request.method == "GET":
        term = request.args
        params = {}
        params["term"] = term.get("artist")
        response = requests.get('https://itunes.apple.com/search?', params = params)
        data = json.loads(response.text)
        r = data["results"]
    return render_template('artist_info.html', objects=r)

@app.route('/artist_links')
def hello_links():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def hello_specificartsts(artist_name):
    term = artist_name
    params = {}
    params["term"] = term
    response = requests.get('https://itunes.apple.com/search?', params = params)
    data = json.loads(response.text)
    item = data["results"]
    return render_template('specific_artist.html', results = item)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
