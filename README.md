### Telegram Bot

#### Description
Coded in Python using `telegram` package. For now the bot has five options: `Set Alert`, `Get price of BTC`, `Get price of ETH`, `Get price of any coin` and `Get new emails`

#### Install
- Run `pip install -r requirements.txt`
- Create a `.env` file with the following variable: `BOT_ID` where you will put the ID of the bot previously created in Telegram.
- In the `.env` you need to set another variable: `COIN_API_KEY` for having access to the API used for get coin prices.
- Add another variable named `USER_ID` and give it the value of your user_id in Telegram.
- For connecting to GMail you need to create a project in GCP and download the credentials file for OAUth 2.0 ID
- You must set the env variable `CREDENTIALS_FILE` and `TOKEN_FILE`, the first one is the name of the downloaded file with the OAuth 2.0 credentials, the second one is the name of the file where the token will be located after the first connection in which you will be requested to authenticate to Google
- You must set also the env variable `GCP_TOKEN_BASE64` which will contain the base64 encoded string of the content of the token file. 
- Run `python bot.py`
