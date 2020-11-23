from flask import Flask, render_template, redirect, request

from api import ZomatoAPI

app = Flask(__name__)


@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/home/location', methods=['GET', 'POST'])
def get_location():
    api = ZomatoAPI()
    location = request.args.get('location')
    location_dict = api.location(location)
    restaurants = api.location_details(location_dict['entity_id'], location_dict['entity_type'])

    return render_template('location.html', location=location, restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True)
