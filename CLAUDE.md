# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automated US ETF trading system based on the Fear & Greed Index (FGI). It's deployed as an AWS Lambda function that runs daily to execute trades on Korea Investment Securities using their API.

## Key Architecture Components

- **Lambda Function**: Dockerized Python 3.12 function that runs on schedule
- **Trading Strategy**: Contrarian trading based on CNN's Fear & Greed Index
  - EXTREME FEAR (≤25): Buy 2 shares
  - FEAR (25-45): Buy 1 share
  - NEUTRAL (45-55): No action
  - GREED (55-75): Sell 1 share
  - EXTREME GREED (≥75): Sell 2 shares
- **Selenium WebDriver**: Used to scrape the FGI value from CNN (dynamic content)
- **ETF Target**: SPYG (SPDR Portfolio S&P 500 Growth ETF) on AMEX

## Common Development Tasks

### Build and Deploy
```bash
# Build the Lambda function (requires AWS SAM CLI)
sam build

# Deploy to AWS
sam deploy

# View Lambda logs
sam logs -n LambdaFunction --stack-name FGI-daily-trader --tail
```

### Local Testing
```bash
# Test Lambda function locally
sam local invoke LambdaFunction
# or
./test.sh
```

### Code Formatting
The project uses Black formatter with VS Code settings. Format on save is enabled. Use these tools:
- **Formatter**: ms-python.black-formatter
- **Max line length**: 160 (for flake8)

## Important Files and Their Purpose

- `lambda_function.py`: Main entry point - orchestrates the trading logic
- `app/tasks/trade.py`: Korea Investment Securities API integration for trading operations
- `app/tasks/feerAndGreed.py`: Web scraping logic to fetch FGI value from CNN
- `app/tasks/discord.py`: Discord webhook notifications for trade alerts
- `app/config.py`: Configuration and secrets management
- `app/secrets.yml`: Contains API keys (not in repo - needs to be created)
- `template.yaml`: AWS SAM template defining Lambda, IAM roles, and scheduler
- `Dockerfile`: Container definition with Chrome headless setup

## Critical Implementation Details

1. **Chrome Headless**: The Lambda environment requires headless Chrome with specific options to avoid bot detection
2. **Token Management**: Access tokens are cached in `/tmp/access_token.json` with expiry checking
3. **Order Execution**: Orders are placed as limit orders, with pending order cancellation if not filled
4. **Timezone**: All operations use Asia/Seoul timezone (KST)
5. **Scheduler**: Runs at 23:00 KST (14:00 UTC) on weekdays only

## Dependencies

- selenium==4.24.0 (with headless Chrome via chrome-installer.sh)
- requests==2.31.0 (API calls)
- PyYAML==6.0.1 (config management)
- pytz==2024.1 (timezone handling)
- webdriver-manager==4.0.2 (Chrome driver management)

## Configuration Requirements

The `app/secrets.yml` file must contain:
- Korea Investment Securities API credentials (API_KEY, SECRET_KEY, HOST, CANO, ACNT_PRDT_CD)
- Discord webhook URL for notifications