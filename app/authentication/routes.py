from models import User,Results, db
from flask import Blueprint, request
from flask_jwt_extended import create_access_token,unset_jwt_cookies, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import  request,jsonify

auth = Blueprint('auth', __name__, template_folder='authentication')

@auth.route('/logintoken', methods=['POST'])
def create_token():
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    
    user = User.query.filter_by(email= email).first()
    
    if user is None:
        return jsonify({"error":"Wrong email or password"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({"error":"Wrong password"}), 401
    
    user_in_results = Results.query.filter_by(user_email=email).first() is not None

    
    access_token = create_access_token(identity=email)
    return jsonify({
        "access_token" : access_token,
        "email": email,  
        "emailInResults": user_in_results,
}),201
    
@auth.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json["email"]
        password = request.json["password"]
        name = request.json["name"]
        phone  = request.json["phone"]
        
        user_exist = User.query.filter_by(email=email).first()
        
        if user_exist:
            return jsonify({"error": "Email already exists"}), 409

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "email": new_user.email,
            "password": new_user.password,
            "name": new_user.name,
            "id": new_user.id,
            "phone":new_user.phone
        }), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
       
    
@auth.route('/profile/<getemail>', methods=['GET'])
@jwt_required() 
def my_profile(getemail):
    if not getemail:
        return jsonify({"error": "Unauthorized Access"}), 401
       
    user = User.query.filter_by(email=getemail).first()
    response_body = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone":user.phone
    }
    return response_body, 201

@auth.route('/profile/<getemail>', methods=['POST','PUT'])
@jwt_required() 
def update_profile(getemail):
    if not getemail:
        return jsonify({"error": "Unauthorized Access"}), 401
       
    user = User.query.filter_by(email=getemail).first()
    
    if not User:
     return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data['name']
    user.phone = data['phone']
    
    db.session.commit()
    response_body = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }

    return response_body, 201

@auth.route('/profile/<email>', methods=['DELETE'])
@jwt_required() 
def delete_user(email):
    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        result = Results.query.filter_by(user_email=email).first()
        if result:
            db.session.delete(result)
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User and related results deleted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@auth.route('/logout', methods=["POST"])
def logout():
    response = jsonify({"msg":"logout successful"})
    unset_jwt_cookies(response)
    return response, 201
    