from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the parent directory to the Python path to import the aws_cli module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aws_cli.services.s3 import S3Service
from aws_cli.services.ec2 import EC2Service

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/s3', methods=['POST'])
def create_s3():
    data = request.get_json()
    bucket_name = data.get('bucket_name')
    region = data.get('region')

    if not bucket_name or not region:
        return jsonify({'success': False, 'message': 'Bucket name and region are required.'}), 400

    s3_service = S3Service(region)
    result = s3_service.create_resource(bucket_name=bucket_name, region=region)
    return jsonify(result)

@app.route('/api/ec2', methods=['POST'])
def create_ec2():
    data = request.get_json()
    image_id = data.get('image_id')
    instance_type = data.get('instance_type')
    key_name = data.get('key_name')
    count = data.get('count', 1)
    region = data.get('region')

    if not all([image_id, instance_type, key_name, region]):
        return jsonify({'success': False, 'message': 'Image ID, instance type, key name, and region are required.'}), 400

    ec2_service = EC2Service(region)
    result = ec2_service.create_resource(
        image_id=image_id,
        instance_type=instance_type,
        key_name=key_name,
        count=int(count),
        region=region
    )
    return jsonify(result)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
