from typing import Any

from flask import Request

from config_processors.config_processor import ConfigProcessor


class SatosaConfigProcessor(ConfigProcessor):
    def __init__(self, config):
        super().__init__(config)

    # TODO - make actual configs for SATOSA
    def get_satosa_saml_sp_cfg(self, remote_entity_data):
        pass

    def get_satosa_saml_idp_cfg(self, remote_entity_data):
        pass

    def get_satosa_oidc_rp_cfg(self, remote_entity_data):
        pass

    def get_satosa_oidc_op_cfg(self, remote_entity_data):
        pass

    def prepare_configuration(self, request: Request) -> dict[str, Any]:
        remote_entity_data = request.json.get("object")
        entity_type = remote_entity_data.get("entity_type")

        match entity_type:
            case "SAML_SP":
                result = self.get_satosa_saml_sp_cfg(remote_entity_data)
            case "SAML_IDP":
                result = self.get_satosa_saml_idp_cfg(remote_entity_data)
            case "OIDC_RP":
                result = self.get_satosa_oidc_rp_cfg(remote_entity_data)
            case "OIDC_OP":
                result = self.get_satosa_oidc_op_cfg(remote_entity_data)
            case _:
                result = {}

        return result
