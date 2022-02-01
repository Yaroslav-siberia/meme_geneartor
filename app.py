from flask import Flask, render_template, jsonify, request
from model_api import get_model_api


app = Flask(__name__)
model_api = get_model_api()

STATIC_PLACEHOLDER_IMG = "/static/images/placeholder-image.png"
HOST = "0.0.0.0"
PORT = 3000
DEBUG = False


@app.route('/')
def index():
    return render_template('index.html', user_image="/static/images/placeholder-image.png")


@app.route('/generate/<category_id>', methods=["GET"])
def generate_meme(category_id: str):
    # read param from web text input
    user_input = request.args.get('text', type=str)

    result_image_path = STATIC_PLACEHOLDER_IMG

    try:
        check, result_image_path = model_api(category_id, user_input)
        if check:
            result_image_path = result_image_path.lstrip('.')
    except:
        result_image_path = STATIC_PLACEHOLDER_IMG

    print(result_image_path)

    resp = jsonify({"user_image": result_image_path})
    return resp


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
