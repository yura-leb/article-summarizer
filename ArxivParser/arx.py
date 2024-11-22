import sys
from Arxiv import Arxiv
import os
from datetime import datetime, timezone

def download_pdfs(keys: list, start: str, end: str, pdf_dir="pdfs"):
    not_downloaded, titles, links = Arxiv.save_pdfs_and_get_pages(start, end, pdf_dir, keys)

    with open(pdf_dir + os.sep + "articles.txt", "w") as f:
        for title, link in zip(titles, links):
            if link not in not_downloaded:
                f.write(title + "\n" + link + "\n\n")
    print()
    print("Articles downloaded")
    print("Not downloaded:", not_downloaded)


def validate_date(start_date: datetime, end_date: datetime):
    """Validate the date format as YYYY-MM-DD."""
    if start_date <= end_date and start_date < datetime.now(timezone.utc):
        return True
    else:
        return False

def validate_directory(directory):
    """Check if the directory exists."""
    return os.path.isdir(directory)

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <start_date> <end_date> <directory>")
        print("<start_date> formatted YYYY-MM-DD")
        print("<end_date>   formatted YYYY-MM-DD")

    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    directory = sys.argv[3]

    if not validate_date(start_date, end_date):
        print(f"Error: Invalid date range")
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