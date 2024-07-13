from  flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Posts, db
from src.constants.http_status_codes import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from flasgger import swag_from
posts = Blueprint("posts",__name__,url_prefix="/api/v1/posts")

@posts.route("/",methods=['POST','GET'])
@jwt_required()
@swag_from('./docs/posts/create_post.yaml', methods=['POST'])
@swag_from('./docs/posts/get_posts.yaml', methods=['GET'])
def handle_posts():
    user_id = get_jwt_identity()

    if request.method == "POST":

        data = request.get_json()

        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'message': 'Title and content are required'}), HTTP_400_BAD_REQUEST


        new_post = Posts(title=data['title'], content=data['content'], user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({'message': 'Post created successfully',"id":new_post.id}), HTTP_200_OK
    
    else:

        page = request.args.get("page",1,type=int)
        per_page = request.args.get("per_page",5,type=int)

        posts = Posts.query.filter_by(user_id = user_id).paginate(page=page,per_page=per_page)

        data = []

        for post in posts.items:

            data.append({
                "id" : post.id,
                "title" : post.title,
                "content" : post.content,
                 "user_id" : post.user_id,
                "created_at" : post.created_at,
                "updated_at" : post.updated_at
            })

        meta = {
            "page" : posts.page,
            "pages": posts.pages,
            "total_count" : posts.total,
            "prev_page" : posts.prev_num,
            "next_page" : posts.next_num,
            "has_next" : posts.has_next,
            "has_prev" : posts.has_prev
        }

        return jsonify({"data":data, "meta":meta}), HTTP_200_OK
    

@posts.get("/<int:id>")
@jwt_required()
@swag_from('./docs/posts/get_post.yaml')
def get_post(id):
    user_id = get_jwt_identity()

    post = Posts.query.filter_by(user_id=user_id,id=id).first()

    if not post:
        return jsonify({"message":"Post not found"}), HTTP_404_NOT_FOUND
    
    return jsonify({
                "id" : post.id,
                "title" : post.title,
                "content" : post.content,
                 "user_id" : post.user_id,
                "created_at" : post.created_at,
                "updated_at" : post.updated_at
            })
            

@posts.put("/<int:id>")
@posts.patch("/<int:id>")
@jwt_required()
@swag_from('./docs/posts/edit_post.yaml', methods=['PUT'])
def edit_post(id):
    user_id = get_jwt_identity()
    post = Posts.query.filter_by(user_id=user_id,id=id).first()

    if not post:
        return jsonify({"message":"Post not found"}), HTTP_404_NOT_FOUND


    title = request.get_json().get("title","")
    content = request.get_json().get("content","")

    post.title = title
    post.content = content

    db.session.commit()

    return jsonify({
        'message': 'Post updated successfully',
        "title":post.title, 
        "content":post.content, 
        "created_at":post.created_at,
        "updated_at":post.updated_at
        }), HTTP_200_OK
    

@posts.delete("/<int:id>")
@jwt_required()
@swag_from('./docs/posts/delete_post.yaml')
def delete_post(id):
    user_id = get_jwt_identity()
    post = Posts.query.filter_by(user_id=user_id,id=id).first()

    if not post:
        return jsonify({"message":"Post not found"}), HTTP_404_NOT_FOUND
    
    db.session.delete(post)
    db.session.commit()

    return jsonify({}),HTTP_204_NO_CONTENT