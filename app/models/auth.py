# import enum
# from dataclasses import dataclass
#
#
#
# @dataclass
# class ExternalAuthToken:
#     access_token: str
#     refresh_token: str
#     expires_in = int
#
#
# class CredentialType(enum.Enum):
#     social = "social"
#     password = "password"
#
#
# @dataclass
# class Credential:
#     type: CredentialType
#
#
# @dataclass
# class PasswordCredential(Credential):
#     password: str
#
#
# @dataclass
# class SocialCredential(Credential):
#     access_token: str
#     provider: SocialAuthProviderType
