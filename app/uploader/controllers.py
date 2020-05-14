import boto3

# Let's use Amazon S3
from flask import Blueprint, request

from app import app


s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_KEY'],
    endpoint_url=app.config['AWS_ENDPOINT_URL'])

mod_uploader = Blueprint("uploader", __name__, url_prefix="/upload")

print("s3 ------> ", s3)


# Set the route and accepted methods
@mod_uploader.route("/profile/", methods=["POST"])
def profile_image():
    payload = request.get_json()
    print(request.files, payload)
    file = request.files['profile_image']
    filename = file.filename.replace(" ", "")
    try:
        s3.upload_fileobj(
            file,
            app.config["AWS_BUCKET_NAME"],
            filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return "failed"

    return "{}/{}/{}".format(app.config["AWS_ENDPOINT_URL"],
                             app.config["AWS_BUCKET_NAME"],
                             filename)
