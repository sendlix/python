"""Shared pytest fixtures for the Sendlix SDK tests."""

from __future__ import annotations

import pytest

from sendlix.proto import auth_pb2


class _DummyChannel:
    def close(self) -> None:
        pass


class _FixtureAuthStub:
    def __init__(self, channel):
        self.channel = channel

    def GetJwtToken(self, request):
        response = auth_pb2.AuthResponse(token="fixture-token")
        response.expires.seconds = 60
        return response


@pytest.fixture(autouse=True)
def patch_grpc_transports(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent tests from opening real network connections."""

    import sendlix.clients.client as client_module
    import sendlix.auth as auth_module

    def metadata_call_credentials(callback):
        return ("metadata", callback)

    def ssl_channel_credentials():
        return "ssl-creds"

    def composite_channel_credentials(channel_creds, call_creds):
        return ("composite", channel_creds, call_creds)

    def secure_channel(host, credentials, options=None):  # noqa: D401
        return _DummyChannel()

    for module in (client_module.grpc, auth_module.grpc):
        monkeypatch.setattr(
            module, "metadata_call_credentials", metadata_call_credentials)
        monkeypatch.setattr(module, "ssl_channel_credentials",
                            ssl_channel_credentials)
        monkeypatch.setattr(
            module, "composite_channel_credentials", composite_channel_credentials)
        monkeypatch.setattr(module, "secure_channel", secure_channel)

    monkeypatch.setattr(auth_module.auth_pb2_grpc, "AuthStub",
                        lambda channel: _FixtureAuthStub(channel))
