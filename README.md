### Telegram Bot

#### Description
Coded in Python using `telegram` package. For now the bot only has four options: `Set Alert`, `Get price of BTC`, `Get price of ETH` and `Get new emails`

#### Install
- Run `pip install -r requirements.txt`
- Create a `.env` file with the following variable: `BOT_ID` where you will put the ID of the bot previously created in Telegram.
- In the `.env` you need to set another variable: `COIN_API_KEY` for having access to the API used for get coin prices.
- Add another variable named `USER_ID` and give it the value of your user_id in Telegram.
- For connecting to GMail you need to create a project in GCP and download the credentials file (credentials.json) for OAUth 2.0 ID
- Run `python bot.py`
