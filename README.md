### Telegram Bot

#### Description

Coded in Python using `telegram` module. For now the bot has six options: `Set Alert`, `Get price of BTC`, `Get price of ETH`, `Get price of any coin`, `Translate Text` and `Ask question to AI (Google Gemma)`

#### Run containerized

- Install Docker
- Run:

```sh
docker build -t [name_for_the_image] .
docker run [name_for_the_image]
```

#### Run manually

- Run `pip install -r requirements.txt`
- Create a `.env` file with the following variable: `BOT_ID` where you will put the ID of the bot previously created in Telegram.
- In the `.env` you need to set another variable: `COIN_API_KEY` for having access to the API used for get coin prices. The API used is this: [COIN API](https://rest.coinapi.io)
- You also need to set `MODEL_API_KEY`,`MODEL_PROVIDER` and `MODEL_IDENTIFIER` for having access to the LLM
- Add another variable named `USER_ID` and give it the value of your user_id in Telegram.
- You must provide the list of commands from `BOT COMMANDS` to your bot in Telegram.
- Run `python bot.py`
