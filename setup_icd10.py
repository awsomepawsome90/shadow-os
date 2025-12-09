#!/usr/bin/env python3
"""
ICD-10 Medical Database Setup Script for Shadow OS

This script orchestrates the complete ICD-10 integration:
1. Downloads official CDC ICD-10-CM codes
2. Formats them for optimal ChromaDB ingestion
3. Loads them into the vector database

Run this script to populate your Shadow OS with medical knowledge.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add backend to path for imports
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))


def check_dependencies():
    """Verify that required packages are installed."""
    print("[*] Checking dependencies...")
    required_packages = [
        "requests",
        "langchain",
        "chromadb",
        "sentence-transformers",
        "google-generativeai"
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)

    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print("[!] Install them with:")
        print(f"    pip install {' '.join(missing)}")
        return False

    print("[+] All dependencies are installed.\n")
    return True


def step_1_download_icd10():
    """Step 1: Download ICD-10 data from CDC."""
    print("\n" + "=" * 80)
    print("STEP 1: DOWNLOAD ICD-10-CM DATA FROM CDC")
    print("=" * 80)

    try:
        from backend.download_icd10_data import download_icd10_from_cdc, parse_icd10_order_file, create_comprehensive_database

        content = download_icd10_from_cdc()
        if not content:
            print("[!] Failed to download ICD-10 data from CDC.")
            return False

        codes = parse_icd10_order_file(content)
        print(f"[+] Parsed {len(codes)} valid ICD-10 codes")

        create_comprehensive_database(codes)
        print("[+] Step 1 Complete: ICD-10 database created")
        return True

    except Exception as e:
        print(f"[!] Error in Step 1: {e}")
        return False


def step_2_ingest_to_chromadb():
    """Step 2: Ingest the formatted data into ChromaDB."""
    print("\n" + "=" * 80)
    print("STEP 2: INGEST ICD-10 DATA INTO CHROMADB")
    print("=" * 80)

    try:
        print("[*] Running ingestion script...")
        # Run the standard ingest_docs.py which will pick up the ICD-10 data
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "backend" / "ingest_docs.py")],
            cwd=str(Path(__file__).parent),
            capture_output=False
        )

        if result.returncode == 0:
            print("[+] Step 2 Complete: Data ingested into ChromaDB")
            return True
        else:
            print("[!] Ingestion failed. Check the error messages above.")
            return False

    except Exception as e:
        print(f"[!] Error in Step 2: {e}")
        return False


def step_3_verify_setup():
    """Step 3: Verify the setup by checking the database."""
    print("\n" + "=" * 80)
    print("STEP 3: VERIFY SETUP")
    print("=" * 80)

    try:
        from langchain_chroma import Chroma
        from langchain_community.embeddings import SentenceTransformerEmbeddings

        chroma_path = Path(__file__).parent / "data" / "chroma_db"

        if not chroma_path.exists():
            print("[!] ChromaDB not found. Ingestion may have failed.")
            return False

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(
            persist_directory=str(chroma_path),
            embedding_function=embedding_function
        )

        count = vectorstore._collection.count()
        print(f"[+] ChromaDB Status: {count} vectors stored")

        if count > 0:
            print("[+] Step 3 Complete: Setup verified successfully!")
            return True
        else:
            print("[!] No vectors found in ChromaDB.")
            return False

    except Exception as e:
        print(f"[!] Error in Step 3: {e}")
        return False


def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "=" * 80)
    print("SETUP COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Start the backend server:")
    print("   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
    print("\n2. In a new terminal, test the system:")
    print("   python test_brain.py")
    print("\n3. Try a medical query:")
    print("   Example: 'What is Type 2 Diabetes?'")
    print("   Example: 'ICD code for pneumonia'")
    print("\n" + "=" * 80)


def main():
    """Main orchestration function."""
    print("\n" + "=" * 80)
    print("SHADOW OS - ICD-10 MEDICAL DATABASE SETUP")
    print("=" * 80)
    print("\nThis script will:")
    print("1. Download official CDC ICD-10-CM codes (74,719 codes)")
    print("2. Format them for ChromaDB ingestion")
    print("3. Load them into your vector database")
    print("4. Verify the setup")

    # Check dependencies
    if not check_dependencies():
        print("[!] Please install missing dependencies and try again.")
        sys.exit(1)

    # Step 1: Download
    if not step_1_download_icd10():
        print("[!] Setup failed at Step 1. Exiting.")
        sys.exit(1)

    # Step 2: Ingest
    if not step_2_ingest_to_chromadb():
        print("[!] Setup failed at Step 2. Exiting.")
        sys.exit(1)

    # Step 3: Verify
    if not step_3_verify_setup():
        print("[!] Setup failed at Step 3. Exiting.")
        sys.exit(1)

    # Print next steps
    print_next_steps()

    print("\n[+] ICD-10 setup is complete. Your Shadow OS now has medical knowledge!")


if __name__ == "__main__":
    main()
