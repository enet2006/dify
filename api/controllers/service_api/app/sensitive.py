import json
from flask_restful import Resource, fields, marshal_with, reqparse, request
from controllers.service_api import api
from controllers.service_api.wraps import validate_app_token
from models.model import App, AppModelConfig
from extensions.ext_database import db
from werkzeug.exceptions import BadRequest


class AppSensitiveApi(Resource):
    
    parameters_fields = {
        "type": fields.String,
        "enabled": fields.Boolean,
        "config": fields.Raw,
    }

    @validate_app_token
    @marshal_with(parameters_fields)
    def get(self, app_model: App):
        app_model_config = app_model.app_model_config
        features_dict = app_model_config.to_dict()

        return features_dict.get(
                "sensitive_word_avoidance", {"enabled": False, "type": "", "configs": []}
            )
    @validate_app_token
    def post(self, app_model: App):
        if request.is_json:
            data = request.get_json()
            model_config = db.session.query(AppModelConfig).filter(AppModelConfig.id == app_model.app_model_config_id).first()
            model_config.sensitive_word_avoidance=json.dumps(data)        
            db.session.commit()
            return {"result": "success"}
        else:
            raise BadRequest("parameter error.")

api.add_resource(AppSensitiveApi, "/sensitive")
