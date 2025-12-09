#!/usr/bin/env python3
"""
Download official ICD-10-CM database from CDC.
This script fetches the latest ICD-10-CM codes from the CDC's official repository.
Source: CDC/NCHS Official ICD-10-CM Files
"""
import requests
from pathlib import Path


def download_icd10_from_cdc():
    """
    Download official ICD-10-CM files from CDC FTP server.
    Returns the raw content if successful, None otherwise.
    """
    print("[+] Downloading official ICD-10-CM database from CDC...")

    # CDC URL for ICD-10-CM Order Files (2025 release)
    url = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2025/icd10cm-order-Jan-2025.txt"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"[+] Fetching from: {url}")
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        # Save raw file
        output_dir = Path(__file__).parent.parent / "data"
        output_dir.mkdir(exist_ok=True)

        raw_file = output_dir / "icd10cm_official_raw.txt"
        raw_file.write_text(response.text, encoding='utf-8')
        print(f"[+] Downloaded {len(response.text)} characters")
        print(f"[+] Saved raw file to: {raw_file}")

        return response.text

    except Exception as e:
        print(f"[!] Error downloading from CDC: {e}")
        print("[!] Please check your internet connection and try again.")
        return None


def parse_icd10_order_file(content):
    """
    Parse the ICD-10-CM order file format.
    Expected format: CODE + whitespace + description
    """
    codes = {}

    for line in content.split('\n'):
        line = line.strip()
        if not line or len(line) < 10:
            continue

        # Split on first whitespace
        parts = line.split(None, 1)

        if len(parts) >= 2:
            code = parts[0].strip()
            description = parts[1].strip()

            # Validate ICD-10 code format
            # Must start with letter and contain digits
            if (code and len(code) >= 3 and
                code[0].isalpha() and
                any(c.isdigit() for c in code)):
                codes[code] = description

    return codes


def create_comprehensive_database(codes):
    """
    Create a comprehensive formatted database file organized by sections.
    """
    output_dir = Path(__file__).parent.parent / "data"
    output_file = output_dir / "icd10_complete_database.txt"

    # Sort codes alphabetically
    sorted_codes = sorted(codes.items(), key=lambda x: x[0])

    with output_file.open('w', encoding='utf-8') as f:
        f.write("ICD-10-CM Complete Official Database\n")
        f.write("=" * 80 + "\n")
        f.write("Source: CDC/NCHS Official ICD-10-CM Files (2025 Release)\n")
        f.write(f"Total codes: {len(sorted_codes)}\n")
        f.write("=" * 80 + "\n\n")

        current_letter = None
        current_category = None
        stats = {}

        for code, description in sorted_codes:
            letter = code[0]

            # Track statistics
            if letter not in stats:
                stats[letter] = 0
            stats[letter] += 1

            # Add letter section headers
            if letter != current_letter:
                f.write(f"\n{'=' * 80}\n")
                f.write(f"SECTION {letter}\n")
                f.write(f"{'=' * 80}\n\n")
                current_letter = letter

            # Add category headers (first 3 characters)
            category = code[:3]
            if category != current_category:
                f.write(f"\n--- {category} Series ---\n\n")
                current_category = category

            # Write the code entry
            f.write(f"{code}: {description}\n")

        # Write statistics at end
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("CODE DISTRIBUTION BY SECTION\n")
        f.write("=" * 80 + "\n")
        for letter in sorted(stats.keys()):
            f.write(f"Section {letter}: {stats[letter]} codes\n")

    print(f"[+] Created comprehensive database with {len(sorted_codes)} codes")
    print(f"[+] Saved to: {output_file}")
    return output_file


def main():
    """Orchestrate the download and processing workflow."""
    print("\n--- ICD-10-CM Database Downloader ---\n")

    # Step 1: Download from CDC
    content = download_icd10_from_cdc()

    if not content:
        print("\n[!] Failed to download from CDC.")
        print("[!] You can manually download from:")
        print("    https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/")
        return False

    # Step 2: Parse the content
    print("\n[+] Parsing ICD-10-CM codes...")
    codes = parse_icd10_order_file(content)
    print(f"[+] Parsed {len(codes)} valid codes")

    # Step 3: Create formatted database
    print("\n[+] Creating formatted database...")
    create_comprehensive_database(codes)

    print("\n--- Download Complete ---")
    print("[+] ICD-10-CM database is ready for ingestion!")
    print("[+] Next: Run 'python backend/ingest_docs.py' to load into ChromaDB")
    return True


if __name__ == "__main__":
    main()
