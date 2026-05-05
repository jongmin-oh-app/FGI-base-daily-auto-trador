#!/bin/bash
STACK_NAME=FGI-daily-trader

# 빌드
sam build

# 로컬 실행
# sam local invoke LambdaFunction

# 배포
sam deploy

sam logs -n LambdaFunction --stack-name $STACK_NAME --tail