import sys, os
import requests
import qrcode
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import time
import pytz

def generate_qr(data):
    """
    Generates and prints a QR code in the terminal using ASCII characters.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Print the QR code in terminal using ASCII characters
    print("\n--- QR Code ---")
    qr.print_ascii()
    print("---------------\n")

def nearest_clock_emoji(dt: datetime) -> str:
    """
    Given a datetime object, returns the nearest clock emoji
    (hour or half-hour).
    """
    hour = dt.hour % 12  # convert to 12-hour format; 0 -> 12
    if hour == 0:
        hour = 12
    minute = dt.minute

    # Decide if closer to the hour or half past
    if minute < 15:
        # closer to the hour
        # Unicode for 1 o'clock is U+1F550, for 2 o'clock U+1F551, ...
        # So offset by hour - 1
        code_point = 0x1F550 + (hour - 1)
    elif minute >= 45:
        # closer to the next hour
        hour = (hour % 12) + 1  # next hour, 12->1
        code_point = 0x1F550 + (hour - 1)
    else:
        # closer to half past
        # Unicode for 1:30 is U+1F55C, 2:30 is U+1F55D, ...
        # offset by hour - 1
        code_point = 0x1F55C + (hour - 1)

    return chr(code_point)

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import sys

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from colorama import Fore, Style, init
import sys
import time

init(autoreset=True)  # Initialize colorama

import time

def sizeof_fmt(num, suffix='B'):
    """Human-readable file size."""
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Y{suffix}"

def upload_file(filepath):
    """
    Uploads a file with colored ASCII progress bar, uploaded size, total size, and speed.
    """
    url = "https://tmpfiles.org/api/v1/upload"

    bar_length = 30  # length of progress bar

    status = "Connecting..."
    sys.stdout.write(f"{Fore.CYAN}{status}{Style.RESET_ALL}\n")
    sys.stdout.flush()

    start_time = None

    def progress_callback(monitor):
        nonlocal start_time
        if start_time is None:
            start_time = time.time()

        bytes_read = monitor.bytes_read
        total_len = monitor.len
        elapsed = time.time() - start_time
        speed = bytes_read / elapsed if elapsed > 0 else 0

        progress = bytes_read / total_len
        filled_length = int(bar_length * progress)

        bar = Fore.GREEN + '█' * filled_length + Fore.WHITE + '░' * (bar_length - filled_length)
        percent_text = f"{progress * 100:6.2f}%"

        uploaded = sizeof_fmt(bytes_read)
        total = sizeof_fmt(total_len)
        speed_str = sizeof_fmt(speed) + "/s"

        sys.stdout.write(
            f"\rUploading: {bar} {percent_text} | {uploaded} / {total} | {speed_str}   "
        )
        sys.stdout.flush()

    try:
        with open(filepath, 'rb') as file_data:
            encoder = MultipartEncoder(
                fields={
                    'file': (os.path.basename(filepath), file_data, 'application/octet-stream')
                }
            )
            monitor = MultipartEncoderMonitor(encoder, progress_callback)

            headers = {'Content-Type': monitor.content_type}

            status = "Uploading..."
            sys.stdout.write(f"\r{Fore.CYAN}{status}{Style.RESET_ALL}\n")
            sys.stdout.flush()

            response = requests.post(url, data=monitor, headers=headers)

        status = "Waiting for server response..."
        sys.stdout.write(f"\n{Fore.YELLOW}{status}{Style.RESET_ALL}\n")
        sys.stdout.flush()

        response.raise_for_status()

        data = response.json()
        if data.get("status") == "success":
            data = data['data']

            print(f"{Fore.GREEN}✅ File uploaded successfully!{Style.RESET_ALL}")
            print(f"🔗 Temporary Link: {data['url']}")

            time_exp = datetime.now() + timedelta(hours=1)
            time_utc = time_exp.astimezone(pytz.utc)
            print(f"{nearest_clock_emoji(time_exp)} Expires at {time_exp.strftime('%I:%M %p')} ({time_utc.strftime('%I:%M %p')} UTC)")

            generate_qr(data['url'])
        else:
            print(f"{Fore.RED}❌ Upload failed: {data.get('message', 'Unknown error')}{Style.RESET_ALL}")
    except requests.exceptions.SSLError as e:
        print(f"{Fore.RED}❌ SSL Error: {e}{Style.RESET_ALL}")
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED}❌ Connection Error: {e}{Style.RESET_ALL}")
        print("Could be a network issue, firewall, or tmpfiles.org service is down.")
    except requests.exceptions.Timeout as e:
        print(f"{Fore.RED}❌ Timeout Error: {e}{Style.RESET_ALL}")
        print("The request took too long to get a response from tmpfiles.org.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}❌ An unexpected request error occurred: {e}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Error: The file '{filepath}' was not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ An unexpected error occurred: {e}{Style.RESET_ALL}")

def main():
    """
    Main function to handle file selection and upload.
    Allows file path as a command-line argument or opens a file dialog.
    """
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Hide the root Tk window
        root = Tk()
        root.withdraw() 
        filepath = askopenfilename(title="Select a file to upload")
        if not filepath:
            print("❌ No file selected, exiting.")
            sys.exit(1)
        root.destroy() # Destroy the Tkinter root window after selection

    upload_file(filepath)

if __name__ == "__main__":
    main()
