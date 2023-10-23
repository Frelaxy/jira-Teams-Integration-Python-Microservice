import os, binascii
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_token_auth(api_token: str = Depends(oauth2_scheme)):
    write_jira_api_token_in_file()
    api_tokens = open("api_tokens").read().splitlines()
    if api_token not in api_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


def generate_api_token():
    clean_file()
    api_token = binascii.hexlify(os.urandom(20)).decode()
    with open("api_tokens", "a") as file:
        file.write(api_token + '\n')
    return api_token


def write_jira_api_token_in_file():
    if not os.path.exists("api_tokens") or os.stat("api_tokens").st_size == 0:
        with open("api_tokens", "w") as file:
            file.write(os.environ['JIRA_API_TOKEN'] + '\n')


def clean_file():
    lines = open("api_tokens").readlines()
    if len(lines) > 13:
        for i in [1,2,3]:
            lines.pop(i)
        with open("api_tokens",'w') as file:
            file.writelines(lines)

