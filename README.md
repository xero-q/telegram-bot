### Telegram Bot

#### Description
Coded in Python using `telegram` package. For now the bot only has two options: `Set Alert` and `Get value of BTC`.

#### Install
- Run `pip install -r requirements.txt`
- Create a `.env` file with the following variable: `BOT_ID` where you will put the ID of the bot previously created in Telegram.
- In the `.env` you need to set another variable: `COIN_API_KEY` for having access to the API used for get coin prices.
- Run `python bot.py`
