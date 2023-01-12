import logging
import botocore
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy, Algorithm


class BzCrypto:
    """Organizes the crypto client and master key provider. Keeps things readable."""

    def __init__(self, kms_key_arn) -> None:
        self.logger = logging.getLogger(__name__)
        botocore_session = botocore.session.Session()
        kms_kwargs = dict(key_ids=[kms_key_arn], botocore_session=botocore_session)
        self.crypto_client = aws_encryption_sdk.EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
        )
        self.master_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(
            **kms_kwargs
        )

    def decrypt_stream_to_bytes(self, encrypted_stream: object) -> bytes:
        try:
            decrypted_data = self.crypto_client.stream(
                mode="decrypt-unsigned",
                source=encrypted_stream,
                key_provider=self.master_key_provider,
            ).read()
        except Exception as e:
            self.logger.error(f"Error decrypting data.")
            raise e
        return decrypted_data

    def encrypt_bytes_to_bytes(self, bytes: object) -> bytes:
        try:
            encrypted_data = self.crypto_client.stream(
                algorithm=Algorithm.AES_256_GCM_HKDF_SHA512_COMMIT_KEY,
                mode="e",
                source=bytes,
                key_provider=self.master_key_provider,
            ).read()
        except Exception as e:
            self.logger.error(f"Error encrypting data.")
            raise e
        return encrypted_data
