from api import run_api


if __name__ == "__main__":
    try:
        run_api()
    except Exception as e:
        print(f"Failed to run api: {e}")
