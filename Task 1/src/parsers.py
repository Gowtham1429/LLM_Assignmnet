from bs4 import BeautifulSoup
from pypdf import PdfReader


def parse_markdown(path):
    file = open(path, "r", encoding="utf-8")
    text = file.read()
    file.close()
    return text


def parse_html(path):
    file = open(path, "r", encoding="utf-8")
    html = file.read()
    file.close()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    return text


def parse_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text = text + page_text + "\n"

    return text


def extract_text(path):
    lower_path = str(path).lower()

    if lower_path.endswith(".md"):
        return parse_markdown(path)
    elif lower_path.endswith(".html") or lower_path.endswith(".htm"):
        return parse_html(path)
    elif lower_path.endswith(".pdf"):
        return parse_pdf(path)
    else:
        raise ValueError("Unsupported file type")
