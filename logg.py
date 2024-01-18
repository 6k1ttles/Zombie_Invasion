from datetime import datetime


def log_time():
    try:
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('etc/log.txt', 'a') as file:
            file.write("Game started: " + formatted_datetime + '\n')

        print(f"Log entry added: {formatted_datetime}")
    except Exception as e:
        print(f"Error writing to log file: {e}")
