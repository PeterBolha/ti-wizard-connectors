import re

from flask import Request
from marshmallow import (Schema, ValidationError, fields, validate,
                         validates_schema)
from marshmallow.validate import OneOf, Regexp

from enums.entity_type import EntityType

entity_types = [e.name for e in EntityType]
SHA_256_HASH_REGEX = re.compile(r"^[A-Fa-f0-9]{64}$")


class BaseSchema(Schema):
    class Meta:
        unknown = "exclude"

    name = fields.Str(required=False)
    description = fields.Str(required=False)

    entity_type = fields.Str(required=True, validate=OneOf(entity_types))
    id_hash = fields.Str(
        required=True,
        validate=Regexp(
            SHA_256_HASH_REGEX,
            error="Invalid id_hash format. Must be a "
            "64-character hexadecimal string ("
            "SHA256 hash).",
        ),
    )


class SamlSchema(BaseSchema):
    entity_id = fields.Str(required=True)
    metadata_url = fields.Url(required=True)


class OidcOpSchema(BaseSchema):
    client_id = fields.Str(required=True)
    discovery_url = fields.Url(required=True)


class OidcRpSchema(BaseSchema):
    print()
    client_id = fields.Str(required=True)
    redirect_uri = fields.Url(required=True)
    dynamic_registration = fields.Bool(required=False)
    client_secret = fields.Str(required=False)

    @validates_schema
    def validate_dynamic_or_secret(self, data, **kwargs):
        dynamic_registration = data.get("dynamic_registration")
        client_secret = data.get("client_secret")

        # Either dynamic_registration or client_secret must be provided
        if not (dynamic_registration or client_secret):
            raise ValidationError(
                "You must specify either 'dynamic_registration' or 'client_secret'.",
                field_names=["dynamic_registration", "client_secret"],
            )


class ValidationResult:
    def __init__(self, has_valid_data: bool, message: str = None):
        self.has_valid_data = has_valid_data
        self.message = message


def validate_data(request: Request) -> ValidationResult:
    r = request.data
    data = request.json.get("object")

    if not data:
        return ValidationResult(
            has_valid_data=False, message="Request must contain remote entity data."
        )

    try:
        base_schema = BaseSchema()
        result = base_schema.load(data)
        entity_type = result.get("entity_type")

        match entity_type:
            case "SAML_SP" | "SAML_IDP":
                saml_schema = SamlSchema()
                result = saml_schema.load(data)
            case "OIDC_RP":
                oidc_rp_schema = OidcRpSchema()
                result = oidc_rp_schema.load(data)
            case "OIDC_OP":
                oidc_op_schema = OidcOpSchema()
                result = oidc_op_schema.load(data)
    except ValidationError as err:
        return ValidationResult(has_valid_data=False, message=err.messages)

    return ValidationResult(has_valid_data=True)
