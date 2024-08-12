import sys
from arxiv import Arxiv
import os
from datetime import datetime

def download_pdfs(keys: list, start: str, end: str, pdf_dir="pdfs"):
    not_downloaded, links = Arxiv.save_pdfs_and_get_pages(start, end, pdf_dir, keys)
    print()
    print("Articles downloaded")
    print("Not downloaded:", not_downloaded)


def validate_date(date_text):
    """Validate the date format as YYYY-MM-DD."""
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_directory(directory):
    """Check if the directory exists."""
    return os.path.isdir(directory)

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <start_date> <end_date> <directory>")
        print("<start_date> formatted YYYY-MM-DD")
        print("<end_date>   formatted YYYY-MM-DD")

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    directory = sys.argv[3]

    if not validate_date(start_date):
        print(f"Error: Start date '{start_date}' is not in the correct format (YYYY-MM-DD).")
        sys.exit(1)

    if not validate_date(end_date):
        print(f"Error: End date '{end_date}' is not in the correct format (YYYY-MM-DD).")
        sys.exit(1)

    if not validate_directory(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")

    full_keys = []
    with open("ArxivParser/keywords.csv", "r") as fin:
        for line in fin:
            full_keys.append(line.strip())

    download_pdfs(full_keys, start_date, end_date, pdf_dir=directory)

if __name__ == "__main__":
    main()