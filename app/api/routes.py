from models import User, Results, db
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask import  request,jsonify
# from flask_restful import object_as_dict



api = Blueprint('api', __name__, template_folder='api')

@api.route('/results', methods=['POST'])
def create_result():
    email = request.json["user_email"]
    total = request.json["total"]
    questions = request.json["questions"]
    attend = request.json["attend"]
    score = request.json["score"]
    quiz_result = request.json['quiz_result']
    user = User.query.filter_by(email=email).first()
    
    if user:
        user_result = Results.query.filter_by(user_email=email).first()

        if user_result:
            user_result.score = score
            user_result.quiz_result = quiz_result
            user_result.total = total
            user_result.questions = questions
            user_result.attend = attend
        else:
            user_result = Results(user_email=email, score=score, quiz_result=quiz_result, total=total, questions=questions, attend=attend)
            db.session.add(user_result)
            
        db.session.commit()
        
        print(request.json)
        return jsonify({
            "email": user_result.user_email,
            "total":user_result.total,
            "questions": user_result.questions,
            "attend":user_result.attend,
            "score": user_result.score,
            "quiz_result" :user_result.quiz_result,
            "id": user_result.id,  
        }), 201
    else:
        return jsonify({"msg": "User not found"}), 404
        
@api.route('/results/<emailid>', methods=['GET'])
@jwt_required() 
def get_results(emailid):
    if not emailid:
        return jsonify({"error": "Unauthorized"}), 401
    see_user = User.query.filter_by(email = emailid).first()
    user = Results.query.filter_by(user_email=emailid).first()
    if see_user is None:
        return jsonify({"msg":"User not found"}), 404
    else:
        if user is None:
            return jsonify({"error": "User has no results to be published"}), 404
    result_data = {
            "email": user.user_email,
            "total":user.total,
            "questions": user.questions,
            "attend":user.attend,
            "score": user.score,
            "quiz_result" :user.quiz_result,
            "id": user.id,  
        }         
    return jsonify({"results": result_data}), 201