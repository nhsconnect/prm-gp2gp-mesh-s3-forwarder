import logging
from os import environ
from os.path import join
from signal import SIGINT, SIGTERM, signal
from sys import stdout

import boto3

from s3mesh.config import ForwarderConfig
from s3mesh.forwarder import MeshConfig, S3Config, build_forwarder_service
from s3mesh.secrets import SsmSecretManager

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def build_mesh_config_from_ssm(ssm, config) -> MeshConfig:
    mesh_client_cert_path = join(config.forwarder_home, "client_cert.pem")
    mesh_client_key_path = join(config.forwarder_home, "client_key.pem")
    mesh_ca_cert_path = join(config.forwarder_home, "ca_cert.pem")

    secret_manager = SsmSecretManager(ssm)

    secret_manager.download_secret(config.mesh_client_cert_ssm_param_name, mesh_client_cert_path)
    secret_manager.download_secret(config.mesh_client_key_ssm_param_name, mesh_client_key_path)
    secret_manager.download_secret(config.mesh_ca_cert_ssm_param_name, mesh_ca_cert_path)

    mesh_mailbox = secret_manager.get_secret(config.mesh_mailbox_ssm_param_name)
    mesh_password = secret_manager.get_secret(config.mesh_password_ssm_param_name)
    mesh_shared_key = secret_manager.get_secret(config.mesh_shared_key_ssm_param_name)

    return MeshConfig(
        url=config.mesh_url,
        mailbox=mesh_mailbox,
        password=mesh_password,
        shared_key=bytes(mesh_shared_key, "utf-8"),
        client_cert_path=mesh_client_cert_path,
        client_key_path=mesh_client_key_path,
        ca_cert_path=mesh_ca_cert_path,
    )


def build_forwarder_from_environment_variables(env_vars=environ):
    config = ForwarderConfig.from_environment_variables(env_vars)
    ssm = boto3.client("ssm", endpoint_url=config.ssm_endpoint_url)

    return build_forwarder_service(
        mesh_config=build_mesh_config_from_ssm(ssm, config),
        s3_config=S3Config(bucket_name=config.s3_bucket_name, endpoint_url=config.s3_endpoint_url),
        poll_frequency_sec=int(config.poll_frequency),
    )


def main():
    logging.basicConfig(stream=stdout, level=logging.INFO, format=LOG_FORMAT)

    forwarder_service = build_forwarder_from_environment_variables()

    def handle_sigterm(signum, frame):
        forwarder_service.stop()

    signal(SIGINT, handle_sigterm)
    signal(SIGTERM, handle_sigterm)

    forwarder_service.start()


if __name__ == "__main__":
    main()
