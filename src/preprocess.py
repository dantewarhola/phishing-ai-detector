'''
src/preprocess.py

Preprocessing utilities for the Phish‑AI detector project.
'''

import re
import email
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import nltk

# Ensure required NLTK data is present
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


def clean_html(text: str) -> str:
    """Remove HTML tags, returning plain text."""
    return BeautifulSoup(text or "", "html.parser").get_text(" ", strip=True)


def strip_headers(raw: str) -> str:
    """Strip email headers, returning only the message payload."""
    try:
        msg = email.message_from_string(raw or "")
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            return payload.decode(errors='ignore')
        return str(payload)
    except Exception:
        return raw or ""


def collapse_whitespace(text: str) -> str:
    """Replace any whitespace sequence (including newlines) with single spaces."""
    return " ".join((text or "").split())


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize a raw email DataFrame to two columns:
      - 'body': cleaned, header‑stripped, HTML‑removed, single‑spaced text (Subject + Body)
      - 'label': integer 0 (legitimate) or 1 (phishing)

    Steps:
    1. Trim whitespace from column names.
    2. Fill missing Subject/Body with empty strings.
    3. Concatenate Subject + Body, strip headers, clean HTML, collapse whitespace.
    4. Map textual labels to integers and drop unknowns.
    5. Drop duplicates and missing.
    """
    # Normalize column names
    df = df.rename(columns={col: col.strip().lower() for col in df.columns})

    # Ensure subject/body exist
    subj_col = 'subject'
    body_col = 'body'
    df[subj_col] = df.get(subj_col, pd.Series([""] * len(df))).fillna("")
    df[body_col] = df.get(body_col, pd.Series([""] * len(df))).fillna("")

    # Combine, clean, and collapse
    df['body'] = (
        df[subj_col] + ' ' + df[body_col]
    ).apply(strip_headers).apply(clean_html).apply(collapse_whitespace)

    # Map labels
    label_map = {'phishing': 1, 'spam': 1, 'legitimate': 0, 'ham': 0, 1: 1, 0: 0}
    df['label'] = df.get('label').map(label_map)

    # Filter valid labels
    df = df[df['label'].isin([0,1])]

    # Select and dedupe
    clean_df = df[['body','label']].dropna().drop_duplicates().reset_index(drop=True)
    return clean_df


if __name__ == '__main__':
    # CLI: merge all CSVs under data/raw into a Parquet
    base = Path(__file__).resolve().parent.parent / 'data' / 'raw'
    out  = Path(__file__).resolve().parent.parent / 'data' / 'dataset.parquet'
    frames = []
    for f in base.glob('*.csv'):
        try:
            df_clean = normalize(pd.read_csv(f))
            frames.append(df_clean)
        except Exception as e:
            print(f"Skipping {f.name}: {e}")
    if frames:
        full = pd.concat(frames, ignore_index=True)
        full.to_parquet(out)
        print(f"Saved unified dataset with {len(full)} examples to {out}")
    else:
        print("No data frames to process.")
