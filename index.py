import os

from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

from test import driver

app = Flask(__name__, static_url_path='/static')
if not os.path.exists(os.path.join(app.instance_path, 'uploads/testA')):
    os.makedirs(os.path.join(app.instance_path, 'uploads/testA'))


@app.route("/", methods=['POST'])
def startProcess():
    name = ""
    try:
        src = request.files['source']
        param = request.args.get("todo")

        path = os.path.join(app.instance_path,
                            'uploads/testA/', secure_filename(src.filename))
        src.save(path)

        name = os.path.splitext(secure_filename(src.filename))[0]
    except:
        return "Source is empty", 400

    try:
        driver(param)
    except:
        return "Some error occurred while processing", 400

    try:
        os.remove(os.path.join(app.instance_path,
                               'uploads/testA', secure_filename(src.filename)))
        return send_file(os.path.join(app.instance_path,
                                      'uploads/', param + "/test_latest/images/" + name + "_fake.png"),
                         attachment_filename=name + ".png")
    except:
        return "Some error occurred while returning image", 418


if __name__ == "__main__":
    app.run(debug=True)
