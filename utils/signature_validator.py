import hmac
from hashlib import sha256

from flask import Request


class SignatureValidator:
    def __init__(self, processors_cfg):
        self.__PROCESSORS_CFG = processors_cfg
        self.__WEBHOOK_SECRET = processors_cfg.get("shared_settings", {}).get(
            "webhook_secret"
        )

    def has_valid_signature(self, request: Request) -> bool:
        signatures_str = request.headers.get("Django-Webhook-Signature-v1", "")
        signatures = signatures_str.split(",")
        timestamp = request.headers.get("Django-Webhook-Request-Timestamp", "")

        has_valid_signature = True
        for signature in signatures:
            digest_payload = bytes(timestamp, "utf8") + b":" + request.data
            digest = hmac.new(
                key=self.__WEBHOOK_SECRET.encode(),
                msg=digest_payload,
                digestmod=sha256,
            )
            has_valid_signature &= hmac.compare_digest(
                digest.hexdigest(), signature
            )

        return has_valid_signature
