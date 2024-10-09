from flask import Blueprint, request,jsonify

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return jsonify(search_users(request.args.to_dict())), 200

def search_users(args):
    user_id = args.get('id')
    name = args.get('name', '').lower()  
    age = args.get('age')
    occupation = args.get('occupation', '').lower()  
    
    if age:
        age = int(age)

    id_matches = []
    name_matches = []
    age_matches = []
    occupation_matches = []
    
    if user_id:
        for user in USERS:
            if user['id'] == user_id:
                id_matches.append(format_user(user))  
                break  

    for user in USERS:
        name_match = name in user['name'].lower() if name else False
        age_match = (user['age'] in range(age - 1, age + 2)) if age else False
        occupation_match = occupation in user['occupation'].lower() if occupation else False
        if name_match:
            name_matches.append(format_user(user))
        if age_match:
            age_matches.append(format_user(user))
        if occupation_match:
            occupation_matches.append(format_user(user))

    results = id_matches + name_matches + age_matches + occupation_matches
    unique_results = []
    seen_ids = set()
    for user in results:
        if user["id"] not in seen_ids:
            seen_ids.add(user["id"])
            unique_results.append(user)

    return unique_results

def format_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "age": user["age"],
        "occupation": user["occupation"]
    }
