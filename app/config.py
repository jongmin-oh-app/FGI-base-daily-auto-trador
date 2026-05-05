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

    # koreainvestment 파라미터 가져오기 (StringList 타입)
    korea_investment_response = ssm.get_parameter(
        Name='koreainvestment',
        WithDecryption=True
    )
    # StringList는 쉼표로 자동 분리되어 문자열로 반환됨
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
    CANO = parameters['korea_investment'][0]  # 계좌번호
    API_KEY = parameters['korea_investment'][1]  # API 키
    SECRET_KEY = parameters['korea_investment'][2]  # 시크릿 키
    HOST = "https://openapi.koreainvestment.com:9443"  # 고정 HOST
    ACNT_PRDT_CD = "01"  # 직접 설정


@dataclass(frozen=True)
class DiscordConfig:
    DISCORD_WEBHOOK = parameters['discord']
