import unittest

from flask import Flask, Request
from flask.testing import EnvironBuilder

from utils.data_validator import validate_data

FULL_VALID_SAML_DATA = {
    "id": 1,
    "name": "example name",
    "description": "example desc",
    "entity_type": "SAML_SP",
    "entity_id": "test_entityid_3",
    "metadata_url": "https://example-metadata-url.com",
    "discovery_url": "",
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "",
    "dynamic_registration": False,
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
    "is_active": False,
    "comment": "",
    "metadata_hash": "some hash",
    "created_at": "2024-11-11T10:40:58.257653Z",
    "updated_at": "2024-11-22T09:19:19.880505Z",
    "created_by": 1,
    "updated_by": 1,
}

REDUCED_VALID_SAML_DATA = {
    "name": "example name",
    "description": "example desc",
    "entity_id": "test_entityid_3",
    "metadata_url": "https://example-metadata-url.com",
    "entity_type": "SAML_SP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

MINIMAL_VALID_SAML_DATA = {
    "entity_id": "test_entityid_3",
    "metadata_url": "https://example-metadata-url.com",
    "entity_type": "SAML_SP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_SAML_DATA_NO_ENTITY_ID = {
    "metadata_url": "https://example-metadata-url.com",
    "entity_type": "SAML_SP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_SAML_DATA_NO_METADATA_URL = {
    "entity_id": "test_entityid_3",
    "entity_type": "SAML_SP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_SAML_DATA_BAD_FORMAT_METADATA_URL = {
    "entity_id": "test_entityid_3",
    "metadata_url": "NOT_URL",
    "entity_type": "SAML_SP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_SAML_DATA_NO_ID_HASH = {
    "metadata_url": "https://example-metadata-url.com",
    "entity_id": "test_entityid_3",
    "entity_type": "SAML_SP",
}

INVALID_SAML_DATA_NO_ENTITY_TYPE = {
    "entity_id": "test_entityid_3",
    "metadata_url": "https://example-metadata-url.co",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_SAML_DATA_UNKNOWN_ENTITY_TYPE = {
    "entity_id": "test_entityid_3",
    "metadata_url": "https://example-metadata-url.co",
    "entity_type": "INVALID_ENTITY_TYPE",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

REDUCED_VALID_OIDC_OP_DATA = {
    "name": "example name",
    "description": "example desc",
    "client_id": "test_entityid_3",
    "discovery_url": "https://example-discovery-url.com",
    "entity_type": "OIDC_OP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

MINIMAL_VALID_OIDC_OP_DATA = {
    "client_id": "test_entityid_3",
    "discovery_url": "https://example-discovery-url.com",
    "entity_type": "OIDC_OP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_OIDC_OP_DATA_NO_CLIENT_ID = {
    "discovery_url": "https://example-discovery-url.com",
    "entity_type": "OIDC_OP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_OIDC_OP_DATA_NO_DISCOVERY_URL = {
    "client_id": "test_entityid_3",
    "entity_type": "OIDC_OP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_OIDC_OP_DATA_BAD_FORMAT_DISCOVERY_URL = {
    "client_id": "test_entityid_3",
    "discovery_url": "NOT_URL",
    "entity_type": "OIDC_OP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

MINIMAL_VALID_OIDC_RP_DYNAMIC_REGISTRATION_DATA = {
    "client_id": "test_entityid_3",
    "redirect_uri": "https://example-redirect-uri.com",
    "dynamic_registration": True,
    "entity_type": "OIDC_RP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

MINIMAL_VALID_OIDC_RP_STATIC_REGISTRATION_DATA = {
    "client_id": "test_entityid_3",
    "client_secret": "secret",
    "redirect_uri": "https://example-redirect-uri.com",
    "dynamic_registration": False,
    "entity_type": "OIDC_RP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}

INVALID_OIDC_RP_STATIC_REGISTRATION_DATA_NO_CLIENT_SECRET = {
    "client_id": "test_entityid_3",
    "redirect_uri": "https://example-redirect-uri.com",
    "dynamic_registration": False,
    "entity_type": "OIDC_RP",
    "id_hash":
        "b943ca408d3a2a4f13b9db8db10afe4c9bf0e323173f498ac188590b0843d8d9",
}


class TestDataValidator(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def create_mock_request(self, json_data):
        builder = EnvironBuilder(method="POST", json=json_data, app=self.app)
        env = builder.get_environ()

        return Request(env)

    def get_webhook_format_data(self, json_data):
        return {"object": json_data}

    def get_validation_result(self, json_data):
        webhook_format_data = self.get_webhook_format_data(json_data)
        request = self.create_mock_request(webhook_format_data)
        return validate_data(request)

    def test_full_valid_saml_data(self):
        validation_result = self.get_validation_result(FULL_VALID_SAML_DATA)
        self.assertEqual(True, validation_result.has_valid_data)

    def test_reduced_valid_saml_data(self):
        validation_result = self.get_validation_result(REDUCED_VALID_SAML_DATA)
        self.assertEqual(True, validation_result.has_valid_data)

    def test_minimal_valid_saml_data(self):
        validation_result = self.get_validation_result(REDUCED_VALID_SAML_DATA)
        self.assertEqual(True, validation_result.has_valid_data)

    def test_invalid_saml_data_no_entity_id(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_NO_ENTITY_ID
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'entity_id': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_saml_data_no_metadata_url(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_NO_METADATA_URL
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'metadata_url': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_saml_data_bad_format_metadata_url(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_BAD_FORMAT_METADATA_URL
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'metadata_url': ['Not a valid URL.']}",
            str(validation_result.message),
        )

    def test_invalid_saml_data_no_id_hash(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_NO_ID_HASH
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'id_hash': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_saml_data_no_entity_type(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_NO_ENTITY_TYPE
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'entity_type': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_saml_data_unknown_entity_type(self):
        validation_result = self.get_validation_result(
            INVALID_SAML_DATA_UNKNOWN_ENTITY_TYPE
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'entity_type': ['Must be one of: SAML_SP, SAML_IDP, OIDC_RP, "
            "OIDC_OP.']}",
            str(validation_result.message),
        )

    def test_minimal_valid_oidc_op_data(self):
        validation_result = self.get_validation_result(
            MINIMAL_VALID_OIDC_OP_DATA
        )
        self.assertEqual(True, validation_result.has_valid_data)

    def test_invalid_oidc_op_data_no_client_id(self):
        validation_result = self.get_validation_result(
            INVALID_OIDC_OP_DATA_NO_CLIENT_ID
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'client_id': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_oidc_op_data_no_discovery_url(self):
        validation_result = self.get_validation_result(
            INVALID_OIDC_OP_DATA_NO_DISCOVERY_URL
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'discovery_url': ['Missing data for required field.']}",
            str(validation_result.message),
        )

    def test_invalid_oidc_op_data_bad_format_discovery_url(self):
        validation_result = self.get_validation_result(
            INVALID_OIDC_OP_DATA_BAD_FORMAT_DISCOVERY_URL
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'discovery_url': ['Not a valid URL.']}",
            str(validation_result.message),
        )

    def test_minimal_valid_oidc_rp_dynamic_registration_data(self):
        validation_result = self.get_validation_result(
            MINIMAL_VALID_OIDC_RP_DYNAMIC_REGISTRATION_DATA
        )
        self.assertEqual(True, validation_result.has_valid_data)

    def test_minimal_valid_oidc_rp_static_registration_data(self):
        validation_result = self.get_validation_result(
            MINIMAL_VALID_OIDC_RP_STATIC_REGISTRATION_DATA
        )
        self.assertEqual(True, validation_result.has_valid_data)

    def invalid_oidc_rp_static_registration_data_no_client_secret(self):
        validation_result = self.get_validation_result(
            INVALID_OIDC_RP_STATIC_REGISTRATION_DATA_NO_CLIENT_SECRET
        )
        self.assertEqual(False, validation_result.has_valid_data)
        self.assertIn(
            "{'discovery_url': ['Not a valid URL.']}",
            str(validation_result.message),
        )


if __name__ == "__main__":
    unittest.main()
