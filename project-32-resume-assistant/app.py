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
    """Dynamically parses web layouts by mimicking browser signatures."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
    }

    try:
        # Strict timeout constraint to prevent terminal hanging
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\n[!] Automated web scraping blocked by remote firewall: {e}")
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
    parser.add_argument("--url", type=str, required=True, help="Target job posting URL")
    args = parser.parse_args()

    webhook_url = "http://localhost:5678/webhook/resume-assistant-pipeline"

    print("[1/3] Extracting text from your resume PDF...")
    resume_text = extract_resume_text(args.resume)

    print("[2/3] Attempting dynamic web extraction from URL...")
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
