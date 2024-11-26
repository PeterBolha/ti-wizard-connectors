from enum import Enum


class EntityType(Enum):
    SAML_SP = ("SAML SP",)
    SAML_IDP = ("SAML IDP",)
    OIDC_RP = ("OIDC RP",)
    OIDC_OP = ("OIDC OP",)
