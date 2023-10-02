from flask import Flask, request, jsonify, session
from create_tour_main import *
from register import *
from login import *
from reset_password import *
from OTP_validation import *
from change_password import *
from Dashboard import CITY_IMAGE_10, STATE_IMAGE_10, SPOT_IMAGE_10, UT_IMAGE_10

app = Flask(__name__)

all_the_tourist_spot = None
days = 0

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    response_data, status = register_user(data)
    return jsonify(response_data), 200


@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    response_data, status_code = login_user(data)
    if status_code == 200:
        session['username'] = data['email']
        if 'username' in session:
            print({session["username"]})

    return jsonify(response_data)


@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    try:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email address is required'}), 400
        if send_otp_email(email):
            return jsonify({'message': 'OTP sent successfully'})
        else:
            return jsonify({'error': 'Failed to send OTP'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/validate_otp', methods=['POST'])
def validate_otp_route():
    try:
        data = request.get_json()
        email = data.get('email')
        entered_otp = data.get('otp')

        if not email or not entered_otp:
            return jsonify({'error': 'Email and OTP are required'}), 400
        if validate_otp(email, entered_otp):
            return jsonify({'message': 'OTP is valid'})
        else:
            return jsonify({'error': 'Invalid OTP'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset_password', methods=['POST'])
def change_password_route():
    try:
        data = request.get_json()
        email = data.get('email')
        newpassword = data.get('newpassword')

        result = change_password(email, newpassword)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@app.route('/create_tour', methods=['POST'])
def create_tour():
    global all_the_tourist_spot, days
    try:
        result = 'something went wrong'
        data = request.get_json()
        city = data.get('city', '').replace(" ", "")
        days = int(data.get('days', ''))

        print(f"Received city: {city}, days: {days}")

        all_the_tourist_spot = fetch_and_sort(city)
        if all_the_tourist_spot:
            print('all_the_tourist_spot is True')
            personalised = create_personalised_trip(all_the_tourist_spot, no_of_days=days)
        else:
            personalised = None
            print("ISSUE WITH fetch_and_sort function")

        if personalised:
            personalized_trip = generate_personalized_trip(personalised, prefixes)
            return jsonify({"result": personalized_trip})
        else:
            return jsonify({"result": "No personalized trip available"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/create_new', methods=['POST'])
def create_new():
    global all_the_tourist_spot, days
    tourist_spot_to_shuffle = all_the_tourist_spot
    random.shuffle(tourist_spot_to_shuffle)
    personalised_again = create_personalised_trip(tourist_spot_to_shuffle, no_of_days=days)
    personalized_trip = generate_personalized_trip(personalised_again, prefixes)
    return jsonify({"result": personalized_trip})


@app.route('/image_to_dashboard', methods=['GET'])
def get_image_data():

    return jsonify({
        'SPOT_IMAGE_10': SPOT_IMAGE_10,
        'CITY_IMAGE_10': CITY_IMAGE_10,
        'STATE_IMAGE_10': STATE_IMAGE_10,
        'UT_IMAGE_3': UT_IMAGE_10
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
