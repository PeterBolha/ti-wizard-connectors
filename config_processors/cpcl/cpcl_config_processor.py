from typing import Any, Dict

from flask import Request

from config_processors.config_processor import ConfigProcessor


class CpclConfigProcessor(ConfigProcessor):
    def __init__(self, config):
        super().__init__(config)

    def get_saml_sp_cpcl(self, data) -> Dict[str, str]:
        return {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "entityid": data.get("entity_id", ""),
            "metadata_url": data.get("metadata_url", ""),
        }

    def get_saml_idp_cpcl(self, data) -> Dict[str, str]:
        return self.get_saml_sp_cpcl(data)

    def get_oidc_rp_cpcl(self, data) -> Dict[str, str]:
        return {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "client_id": data.get("client_id", ""),
            "client_secret": data.get("client_secret", ""),
            "redirect_uri": data.get("redirect_uri", ""),
            "dynamic_registration": data.get("dynamic_registration", ""),
        }

    def get_oidc_op_cpcl(self, data) -> Dict[str, str]:
        return {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "discovery_url": data.get("discovery_url", ""),
        }

    def prepare_configuration(self, request: Request) -> dict[str, Any]:
        remote_entity_data = request.json.get("object")
        entity_type = remote_entity_data.get("entity_type")

        match entity_type:
            case "SAML_SP":
                result = self.get_saml_sp_cpcl(remote_entity_data)
            case "SAML_IDP":
                result = self.get_saml_idp_cpcl(remote_entity_data)
            case "OIDC_RP":
                result = self.get_oidc_rp_cpcl(remote_entity_data)
            case "OIDC_OP":
                result = self.get_oidc_op_cpcl(remote_entity_data)
            case _:
                result = {}

        return result
