# -*- coding: utf-8 -*-
"""NIYITEGEKA Isaie 2401000694.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11u5_fIt8fMHfPSsnXDGH5yxpQPLv9Jvm
"""

import pandas as pd


file_path = "/content/2401000694 emails_exercises.csv"


try:
    emails = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at '{file_path}'. Please check the file path and make sure the file exists.")
else:

    phishing_keywords = ["urgent", "password reset", "bank", "verify", "account suspended"]
    if "Content" in emails.columns:
        emails["is_phishing"] = emails["Content"].apply(lambda x: any(keyword in str(x).lower() for keyword in phishing_keywords))
        emails.to_csv("/content/2401000694 emails_exercises.csv", index=False)
        print("phishing detection complete. True")
    else:
        print("Error: The 'content' column is missing from dataset.")