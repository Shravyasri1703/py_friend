from app import app, db
from flask import request, jsonify
from models import Freind

@app.route('/api/freinds',methods=["GET"])
def get_freinds():
    freinds = Freind.query.all()
    result = [friend.to_json() for friend in freinds]
    return jsonify(result), 200

@app.route('/api/freinds',methods=["POST"])
def creat_freind():

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    try:
        data = request.json

        required_fields = ["name","role","description","gender"]
        for field in required_fields:
           if field not in data or not data.get(field):
            return jsonify({"error":f'Missing required field: {field}'}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None
        
        new_freind = Freind(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_freind)
        db.session.commit()

        return jsonify({"msg":"freind added"}, new_freind.to_json()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    

@app.route('/api/freinds/<int:id>',methods=["DELETE"])
def deleteFreind(id):
    try:
        friend = Freind.query.get(id)
        if friend is None:
            return jsonify({"error":"Friend not found"}), 404
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message":"Friend deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500


@app.route("/api/freinds/<int:id>", methods=['PATCH']) 
def update_freinds(id):
    try:
        friend = Freind.query.get(id)
        if friend is None:
            return jsonify({"error":"Freind not found"}), 404
        data = request.json

        friend.name = data.get("name",friend.name)
        friend.role = data.get("role",friend.role)
        friend.description = data.get("description",friend.description)
        friend.gender = data.get("gender",friend.gender)

        db.session.commit()

        return jsonify(friend.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

