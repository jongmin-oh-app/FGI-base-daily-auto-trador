from typing import Final
from pathlib import Path
from dataclasses import dataclass

import boto3

CRAWL_URL: Final[str] = "https://edition.cnn.com/markets/fear-and-greed"
TIME_OUT: Final[int] = 10


@dataclass(frozen=True)
class Paths:
    BASE_DIR: Path = Path(__file__).resolve().parent
    ACCESS_TOKEN_PATH: Path = BASE_DIR.joinpath("/tmp/access_token.json")


def get_parameters_from_store():
    """AWS Parameter Store에서 파라미터 가져오기"""
    ssm = boto3.client('ssm', region_name='ap-northeast-2')

    # koreainvestment 파라미터 가져오기
    korea_investment_response = ssm.get_parameter(
        Name='koreainvestment',
        WithDecryption=True
    )
    korea_investment_values = korea_investment_response['Parameter']['Value'].split(',')

    # discord 파라미터 가져오기
    discord_response = ssm.get_parameter(
        Name='discord',
        WithDecryption=True
    )
    discord_value = discord_response['Parameter']['Value']

    return {
        'korea_investment': korea_investment_values,
        'discord': discord_value
    }


# Parameter Store에서 값 가져오기
parameters = get_parameters_from_store()


@dataclass(frozen=True)
class Config:
    API_KEY = parameters['korea_investment'][0]
    SECRET_KEY = parameters['korea_investment'][1]
    HOST = parameters['korea_investment'][2]
    CANO = parameters['korea_investment'][3]
    ACNT_PRDT_CD = parameters['korea_investment'][4]


@dataclass(frozen=True)
class DiscordConfig:
    DISCORD_WEBHOOK = parameters['discord']
