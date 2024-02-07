from bot.helper import Bot


if __name__ == "__main__":
    try:
        Bot.run_app_bot()
    except Exception as e:
        print(f"Failed to run bot: {e}")
