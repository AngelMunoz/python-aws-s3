import os
import tempfile
from os import path
from flask import Flask, jsonify, request, send_file
import boto3

# Let's use Amazon S3
app = Flask(__name__)

s3 = boto3.resource('s3')


@app.route('/')
def root():
    return jsonify(message='Hello World!'), 200


@app.route('/list-buckets')
def list_buckets():

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    return ''


@app.route('/save-file', methods=['POST'])
def save_file():
    file = request.files['file']

    temp = tempfile.NamedTemporaryFile(delete=False)
    # save the file in a temporary dir
    file.save(temp.name)

    # Upload the file
    s3.Bucket('treesito-dev').put_object(Key='test.png', Body=temp)

    # Clean-up temp file
    os.remove(temp.name)
    print(f'Saved FIle')
    return '', 200


@app.route('/download-file')
def download_file():

    with open(tempfile.NamedTemporaryFile().name, 'w+b') as f:
        s3.Bucket('treesito-dev').download_file("test.png", f.name)

    return send_file(f.name, mimetype="image/png", as_attachment=True)


@app.route('/see-file')
def see_file():
    with open(tempfile.NamedTemporaryFile().name, 'w+b') as f:
        s3.Bucket('treesito-dev').download_file("test.png", f.name)

    return send_file(f.name, mimetype="image/png", as_attachment=False)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
