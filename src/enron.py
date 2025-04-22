import pandas as pd
import email
from bs4 import BeautifulSoup

# enron.py
# Script to load and clean the Enron phishing dataset.

# Helper functions

def collapse_whitespace(text: str) -> str:
    """Replace CRLF/newlines and collapse multiple spaces into single spaces."""
    return ' '.join((text or "").replace('\r\n', ' ').split())


def strip_headers(raw: str) -> str:
    """Strip email headers, returning only the message body."""
    try:
        msg = email.message_from_string(raw or "")
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            return payload.decode(errors='ignore')
        return str(payload)
    except Exception:
        return raw or ""


def clean_html(text: str) -> str:
    """Remove HTML tags and return plain text."""
    return BeautifulSoup(text or "", "lxml").get_text(" ", strip=True)


def clean_text(text: str) -> str:
    """Full pipeline: strip headers, remove HTML, collapse whitespace."""
    no_headers = strip_headers(text)
    no_html = clean_html(no_headers)
    return collapse_whitespace(no_html)


if __name__ == '__main__':
    # 1) Load the raw Enron data
    df = pd.read_csv("data/raw/Enron.csv")

    # 2) Fill missing values and combine subject + body
    df['subject'] = df['subject'].fillna('')
    df['body'] = df['body'].fillna('')
    df['raw_text'] = df['subject'] + ' ' + df['body']

    # 3) Apply cleaning pipeline
    df['clean_text'] = df['raw_text'].apply(clean_text)

    # 4) Sanity-check: show before vs. after for the first email
    print("Before (raw):")
    print(df.loc[0, 'raw_text'][:200])
    print("\nAfter (clean):")
    print(df.loc[0, 'clean_text'][:200])

    # 5) Label distribution
    print("\nLabel distribution:")
    print(df['label'].value_counts())