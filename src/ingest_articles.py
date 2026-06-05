from pypdf import PdfReader
import re


def extract_text(pdf_path):
    """
    Extract text from PDF.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def split_articles(text):
    """
    Split Constitution text into article-like chunks.

    This is a first attempt and is meant for inspection.
    """

    pattern = r'\n(?=\d+\.\s)'

    articles = re.split(pattern, text)

    return articles


def clean_articles(article_chunks):

    cleaned = []

    for chunk in article_chunks:

        chunk = chunk.strip()

        if len(chunk) < 100:
            continue

        cleaned.append(chunk)

    return cleaned


def main():

    pdf_path = r"D:\MTech\Projects\LegalGPT-India\data\constitution.pdf"

    print("=" * 60)
    print("Reading Constitution PDF")
    print("=" * 60)

    text = extract_text(pdf_path)

    print(f"Characters extracted: {len(text):,}")

    print("\nSplitting articles...")

    articles = split_articles(text)

    cleaned_articles = clean_articles(articles)

    print(f"\nRaw article chunks: {len(articles)}")
    print(f"Cleaned article chunks: {len(cleaned_articles)}")

    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS")
    print("=" * 60)

    start = 20
    end = 30

    for i in range(start, end):

        print("\n")
        print("=" * 60)
        print(f"ARTICLE CHUNK {i}")
        print("=" * 60)

        print(cleaned_articles[i][:1500])

        print("\n")

    print("\nFinished.")


if __name__ == "__main__":
    main()