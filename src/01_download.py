"""
Download the UCI Online Retail dataset.
Source: https://archive.ics.uci.edu/ml/datasets/Online+Retail
Saves raw file to data/online_retail_raw.xlsx
"""
import pathlib
import urllib.request

RAW_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "00352/Online%20Retail.xlsx"
)
OUTPUT = pathlib.Path("data/online_retail_raw.xlsx")

def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    if OUTPUT.exists():
        print(f"Already downloaded: {OUTPUT}")
        return
    print("Downloading UCI Online Retail dataset (~23 MB)…")
    urllib.request.urlretrieve(RAW_URL, OUTPUT)
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
