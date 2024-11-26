from http import HTTPStatus
from typing import List

from flask import Flask, Request, Response, request

from config_processors.config_processor import ConfigProcessor
from config_processors.config_processors_initializer import \
    ConfigProcessorsInitializer
from utils.config_loader import ConfigLoader
from utils.data_validator import validate_data
from utils.signature_validator import SignatureValidator


def set_flask_config_options(app: Flask, app_cfg) -> None:
    app.config["HOST"] = app_cfg.get("host", "0.0.0.0")
    app.config["PORT"] = app_cfg.get("port", 5000)


def get_flask_app() -> Flask:
    processors_cfg = ConfigLoader.load_config()

    app = Flask(__name__)
    set_flask_config_options(app, processors_cfg.get("flask_settings", {}))

    config_processors_initializer = ConfigProcessorsInitializer(processors_cfg)
    signature_validator = SignatureValidator(processors_cfg)
    config_processors = config_processors_initializer.get_processors()

    def get_relevant_config_processors(
            request: Request,
    ) -> List[ConfigProcessor]:
        received_hash_id = request.json.get("object", {}).get("id_hash")
        relevant_config_processors = []
        for config_processor in config_processors:
            observed_entity_filters = config_processor.observed_entity_filters
            # special case where no entity filters are configured ->
            # config_processor is relevant for all entities
            if not observed_entity_filters:
                relevant_config_processors.append(config_processor)
                continue

            if received_hash_id in observed_entity_filters:
                relevant_config_processors.append(config_processor)
                continue

        return relevant_config_processors

    def update_relevant_configurations(request: Request) -> None:
        relevant_config_processors = get_relevant_config_processors(request)

        # TODO - handle errors when updating configuration (missing attrs etc.)
        for config_processor in relevant_config_processors:
            config_processor.update_configuration(request)

    @app.route("/remote-entity-update", methods=["POST"])
    def remote_entity_update():
        if not signature_validator.has_valid_signature(request):
            return Response(
                "Invalid signature on received data",
                status=HTTPStatus.UNAUTHORIZED,
            )

        validator_result = validate_data(request)
        if not validator_result.has_valid_data:
            return Response(
                f"Invalid data: {validator_result.message}",
                status=HTTPStatus.BAD_REQUEST,
            )

        update_relevant_configurations(request)

        return Response("Webhook received.", status=HTTPStatus.OK)

    return app


if __name__ == "__main__":
    app = get_flask_app()
    app.run(host=app.config["HOST"], port=app.config["PORT"])
