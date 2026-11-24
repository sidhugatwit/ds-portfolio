import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
import pypdf


def extract_resume_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Resume PDF not found at: {pdf_path}")
    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def scrape_job_description_dynamically(url):
    """Fetch a public job posting page and return its readable text, or None if blocked."""
    # Identify honestly. Many job boards forbid scraping; if a site blocks this,
    # use --job-file with the pasted posting instead of working around it.
    headers = {"User-Agent": "resume-assistant/1.0 (personal portfolio project)"}

    try:
        # Strict timeout constraint to prevent terminal hanging
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\n[!] Could not fetch the posting: {e}")
        print("[-] Falling back to manual cache validation sequence...")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Strip layout noise natively
    for element in soup(
        ["script", "style", "nav", "footer", "header", "form", "iframe"]
    ):
        element.decompose()

    cleaned_text = "\n".join(
        line.strip() for line in soup.get_text().splitlines() if line.strip()
    )

    # Dynamically cache the file locally for audit trailing
    cache_path = os.path.join("data", "dynamic_job_cache.txt")
    os.makedirs("data", exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(
        f"[+] Web content parsed successfully and cached dynamically at: {cache_path}"
    )
    return cleaned_text


def main():
    parser = argparse.ArgumentParser(description="Dynamic Resume Assistant Client")
    parser.add_argument("--resume", type=str, required=True, help="Path to resume PDF")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--job-file", type=str, help="Text file with the pasted job posting (recommended)")
    source.add_argument("--url", type=str, help="Public job posting URL")
    args = parser.parse_args()

    webhook_url = os.getenv(
        "RESUME_WEBHOOK_URL", "http://localhost:5678/webhook/resume-assistant-pipeline"
    )

    print("[1/3] Extracting text from your resume PDF...")
    resume_text = extract_resume_text(args.resume)

    if args.job_file:
        print("[2/3] Reading the job posting from file...")
        with open(args.job_file, "r", encoding="utf-8") as f:
            job_text = f.read().strip()
    else:
        print("[2/3] Fetching the job posting from URL...")
        job_text = scrape_job_description_dynamically(args.url)

    # Fail-safe check: If blocked, prompt user to use the cached local file override
    if not job_text:
        print(
            "\n[Action Required] Please copy the job text manually into 'data/dynamic_job_cache.txt'"
        )
        input("Press Enter once the file is saved to resume the API pipeline...")
        with open(
            os.path.join("data", "dynamic_job_cache.txt"), "r", encoding="utf-8"
        ) as f:
            job_text = f.read().strip()

    payload = {"resumeContent": resume_text, "jobDescription": job_text}

    print("[3/3] Forwarding live payload to production n8n webhook...")
    try:
        response = requests.post(webhook_url, json=payload, timeout=60)
        response.raise_for_status()
        print("\n=== Success Response From Pipeline ===")
        print(response.text)
    except requests.RequestException as e:
        print(f"\nPipeline execution failed: {e}")


if __name__ == "__main__":
    main()
