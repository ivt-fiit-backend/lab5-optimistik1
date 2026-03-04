import json
import os
from flask import Flask, abort, request, jsonify
from flask_restx import Api, Resource # type: ignore

PAGE_SIZE = 25

app = Flask(__name__)
api = Api(app)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'awards.json'), encoding='utf-8') as f:
    awards = json.load(f)

with open(os.path.join(BASE_DIR, 'laureats.json'), encoding='utf-8') as f:
    laureats = json.load(f)


@app.route("/api/v1/awards/")
def awards_list():
    try:
        p = int(request.args.get('p', 0))
        if p < 0:
            raise ValueError
    except ValueError:
        abort(400)

    page = awards[p * PAGE_SIZE:(p + 1) * PAGE_SIZE]

    return jsonify({
        'page': p,
        'count_on_page': len(page),
        'total': len(awards),
        'items': page,
    })


@app.route("/api/v1/award/<int:pk>/")
def award_object(pk):
    if 0 <= pk < len(awards):
        return jsonify(awards[pk])
    else:
        abort(404)


@api.route("/v2/laureats/")
class LaureatsList(Resource):
    def get(self):
        return {
            "total": len(laureats),
            "items": laureats
        }, 200


@api.route("/v2/laureat/<int:pk>/")
class LaureatObject(Resource):
    def get(self, pk):
        if 0 <= pk < len(laureats):
            return laureats[pk], 200
        else:
            abort(404)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
