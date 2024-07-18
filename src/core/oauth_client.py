import ssl
from urllib import parse

import aiohttp
import certifi

from .exceptions import InvalidAuthorizationCode, InvalidToken


class OAuthClient:
    def __init__(
            self,
            client_id,
            client_secret_id,
            redirect_uri,
            authentication_uri,
            resource_uri,
            verify_uri,
    ) -> None:
        self._client_id = client_id
        self._client_secret_id = client_secret_id
        self._redirect_uri = redirect_uri
        self._authentication_uri = authentication_uri
        self._resource_uri = resource_uri
        self._verify_uri = verify_uri
        self._header_name = "Authorization"
        self._header_type = "Bearer"

    def _get_connector_for_ssl(self) -> aiohttp.TCPConnector:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        return aiohttp.TCPConnector(ssl=ssl_context)

    async def _request_get_to(self, url: str, headers=None) -> dict | None:
        conn = self._get_connector_for_ssl()
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(url, headers=headers) as resp:
                return None if resp.status != 200 else await resp.json()

    async def _request_post_to(self, url: str, payload=None) -> dict | None:
        conn = self._get_connector_for_ssl()
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(url, data=payload) as resp:
                return None if resp.status != 200 else await resp.json()

    def get_oauth_login_url(self, state: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "state": state,
        }
        query_param = parse.urlencode(params, doseq=True)

        return f"{self._authentication_uri}/authorize?{query_param}"

    async def get_tokens(self, code: str, state: str) -> dict:
        tokens = await self._request_post_to(
            url=f"{self._authentication_uri}/token",
            payload={
                "client_id": self._client_id,
                "client_secret": self._client_secret_id,
                "grant_type": "authorization_code",
                "code": code,
                "state": state,
            },
        )
        if tokens is None:
            raise InvalidAuthorizationCode

        if tokens.get("access_token") is None or tokens.get("refresh_token") is None:
            raise InvalidAuthorizationCode

        return tokens

    async def refresh_access_token(self, refresh_token: str) -> dict:
        tokens = await self._request_post_to(
            url=f"{self._authentication_uri}/token",
            payload={
                "client_id": self._client_id,
                "client_secret": self._client_secret_id,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )
        if tokens is None:
            raise InvalidToken
        return tokens

    async def get_user_info(self, access_token: str) -> dict:
        headers = {self._header_name: f"{self._header_type} {access_token}"}
        user_info = await self._request_get_to(url=self._resource_uri, headers=headers)
        if user_info is None:
            raise InvalidToken
        return user_info

    async def is_authenticated(self, access_token: str) -> bool:
        headers = {self._header_name: f"{self._header_type} {access_token}"}
        res = await self._request_get_to(
            url=self._verify_uri,
            headers=headers,
        )
        return res is not None


naver_client = OAuthClient(
    client_id="your_client_id",
    client_secret_id="your_client_secret_id",
    redirect_uri="your_callback_uri",
    authentication_uri="https://nid.naver.com/oauth2.0",
    resource_uri="https://openapi.naver.com/v1/nid/me",
    verify_uri="https://openapi.naver.com/v1/nid/verify",
)
