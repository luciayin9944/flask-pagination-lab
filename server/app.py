#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

# class Books(Resource):
#     def get(self):
#         # books = [BookSchema().dump(b) for b in Book.query.all()]
#         books = [BookSchema().dump(b) for b in Book.query.limit(30).all()]
#         return books, 200


#pagination
class Books(Resource):
    def get(self):
        # Step 1: Get query parameters (default to page 1, 5 per page)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # Step 2: Paginate the query with SQLAlchemy's 'paginate()'
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        books = pagination.items

        # Step 3: Return both items and pagination metadata
        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": [BookSchema().dump(book) for book in books]
        }, 200



api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    #print(app.url_map)
    app.run(port=5555, debug=True)