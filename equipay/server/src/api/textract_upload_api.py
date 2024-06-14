from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
import boto3
import re
from werkzeug.datastructures import FileStorage

class UploadAndAnalyzeAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location='files', required=True, help="File is required")
        self.textract = boto3.client('textract')

    def post(self):
        args = self.parser.parse_args()
        file = args['file']
        
        if file:
            file_contents = file.read()
            response = self.textract.analyze_document(
                Document={'Bytes': file_contents},
                FeatureTypes=['FORMS', 'TABLES']
            )

            lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
            print(lines)  

            shop_name = lines[0] if lines else None  
            total_amount = None

            total_patterns = r'\b(TOTAL|Total|\*\*\*\* TOTAL)\b'
            for i, line in enumerate(lines):
                if re.search(total_patterns, line, re.IGNORECASE):
                    amount_match = re.search(r'\d+\.\d+', line)
                    if not amount_match and i + 1 < len(lines):
                        next_line = lines[i + 1]
                        amount_match = re.search(r'\d+\.\d+', next_line)
                    if amount_match:
                        total_amount = amount_match.group(0)
                        break

            # Return results
            return jsonify(shop_name=shop_name, total_amount=total_amount) if total_amount else make_response(jsonify({"error": "No relevant data found"}), 404)

        return make_response(jsonify({"error": "No file uploaded"}), 400)
