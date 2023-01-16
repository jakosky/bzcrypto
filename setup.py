from setuptools import setup

setup(
    name="bzcrypto",
    version="0.0.1",
    url="",
    author="Jay Jakosky",
    author_email="jay.jakosky@gmail.com",
    description="Shared AWS KMS encryption/decryption library for Bozzetti",
    packages=["bzcrypto"],
    install_requires=["botocore >= 1.29.24", "aws-encryption-sdk >= 3.1.1"],
)
