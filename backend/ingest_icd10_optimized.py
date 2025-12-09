#!/usr/bin/env python3
"""
Optimized ICD-10 Ingestion Script for Shadow OS

EFFICIENCY OPTIMIZATIONS:
1. Larger chunk size (1000 chars) = fewer vectors = faster search
2. Groups related codes by category for better semantic matching
3. Batch processing for faster ingestion
4. Minimal chunk overlap to reduce redundancy
5. Pre-filters unnecessary formatting/headers
"""
import os
import re
import time
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

# --- Configuration ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = Path(__file__).parent.parent / "data" / "chroma_db"
ICD10_DATA_PATH = Path(__file__).parent.parent / "data" / "icd10_database.txt"

# EFFICIENCY SETTINGS
CHUNK_SIZE = 1000       # Larger chunks = fewer vectors = faster retrieval
BATCH_SIZE = 500        # Process in large batches for speed
MIN_CHUNK_LENGTH = 50   # Skip tiny chunks


def parse_icd10_codes(content: str) -> dict:
    """
    Parse ICD-10 codes into category groups for efficient chunking.
    Returns dict: {category: [(code, description), ...]}
    """
    categories = {}
    current_category = None

    # Pattern to match code entries
    code_pattern = re.compile(r'^Code:\s*([A-Z0-9.]+)\s*$', re.MULTILINE)
    desc_pattern = re.compile(r'^Description:\s*(.+)\s*$', re.MULTILINE)

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Track category headers
        if line.startswith('--- Category'):
            match = re.search(r'Category ([A-Z0-9]+)', line)
            if match:
                current_category = match.group(1)
                if current_category not in categories:
                    categories[current_category] = []

        # Extract code entries
        if line.startswith('Code:'):
            code = line.replace('Code:', '').strip()
            # Look for description on next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('Description:'):
                    desc = next_line.replace('Description:', '').strip()
                    cat = current_category or code[:3]
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append((code, desc))
        i += 1

    return categories


def create_optimized_chunks(categories: dict) -> list:
    """
    Create optimized chunks by grouping related codes together.
    This improves semantic matching for medical queries.
    """
    chunks = []

    # Medical category names for better context
    category_names = {
        'A': 'Infectious diseases', 'B': 'Infectious diseases',
        'C': 'Neoplasms (Cancer)', 'D': 'Blood diseases and Neoplasms',
        'E': 'Endocrine, nutritional and metabolic diseases',
        'F': 'Mental and behavioral disorders',
        'G': 'Nervous system diseases',
        'H': 'Eye and ear diseases',
        'I': 'Circulatory system diseases',
        'J': 'Respiratory system diseases',
        'K': 'Digestive system diseases',
        'L': 'Skin diseases',
        'M': 'Musculoskeletal diseases',
        'N': 'Genitourinary system diseases',
        'O': 'Pregnancy and childbirth',
        'P': 'Perinatal conditions',
        'Q': 'Congenital malformations',
        'R': 'Symptoms and signs',
        'S': 'Injury', 'T': 'Injury and poisoning',
        'V': 'External causes', 'W': 'External causes',
        'X': 'External causes', 'Y': 'External causes',
        'Z': 'Health services encounters'
    }

    for category, codes in sorted(categories.items()):
        if not codes:
            continue

        # Get category context
        letter = category[0] if category else 'X'
        cat_name = category_names.get(letter, 'Medical codes')

        # Build chunk content
        chunk_content = []
        current_chunk = f"ICD-10 Category {category} - {cat_name}:\n"

        for code, desc in codes:
            entry = f"{code}: {desc}\n"

            # If adding this entry exceeds chunk size, save current and start new
            if len(current_chunk) + len(entry) > CHUNK_SIZE:
                if len(current_chunk) > MIN_CHUNK_LENGTH:
                    chunks.append(current_chunk.strip())
                current_chunk = f"ICD-10 Category {category} - {cat_name} (continued):\n"

            current_chunk += entry

        # Don't forget the last chunk
        if len(current_chunk) > MIN_CHUNK_LENGTH:
            chunks.append(current_chunk.strip())

    return chunks


def clear_existing_db():
    """Clear existing ChromaDB to ensure clean ingestion."""
    if CHROMA_DB_PATH.exists():
        import shutil
        print("[*] Clearing existing ChromaDB...")
        try:
            shutil.rmtree(CHROMA_DB_PATH)
            print("[+] Database cleared.")
        except PermissionError:
            print("[!] Database locked - will add to existing data instead.")


def main():
    """Main optimized ingestion workflow."""
    start_time = time.time()

    print("\n" + "=" * 60)
    print("SHADOW OS - OPTIMIZED ICD-10 INGESTION")
    print("=" * 60)
    print("\nEfficiency optimizations enabled:")
    print(f"  - Chunk size: {CHUNK_SIZE} chars (larger = faster search)")
    print(f"  - Batch size: {BATCH_SIZE} docs")
    print(f"  - Category grouping for semantic matching")
    print()

    # Step 1: Load data
    print("[1/5] Loading ICD-10 data...")
    if not ICD10_DATA_PATH.exists():
        print(f"[!] ERROR: {ICD10_DATA_PATH} not found!")
        print("[!] Run the download script first.")
        return False

    content = ICD10_DATA_PATH.read_text(encoding='utf-8')
    print(f"      Loaded {len(content):,} characters")

    # Step 2: Parse codes
    print("[2/5] Parsing ICD-10 codes by category...")
    categories = parse_icd10_codes(content)
    total_codes = sum(len(codes) for codes in categories.values())
    print(f"      Found {total_codes:,} codes in {len(categories)} categories")

    # Step 3: Create optimized chunks
    print("[3/5] Creating optimized chunks...")
    chunks = create_optimized_chunks(categories)
    print(f"      Created {len(chunks):,} optimized chunks")
    print(f"      Average chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars")

    # Step 4: Clear and initialize ChromaDB
    print("[4/5] Initializing ChromaDB...")
    clear_existing_db()

    embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embedding_function
    )

    # Step 5: Batch ingest
    print(f"[5/5] Ingesting {len(chunks):,} chunks in batches of {BATCH_SIZE}...")

    documents = [Document(page_content=chunk, metadata={"source": "ICD-10-CM"}) for chunk in chunks]

    total_batches = (len(documents) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        vectorstore.add_documents(batch)
        print(f"      Batch {batch_num}/{total_batches} complete ({len(batch)} docs)")

    # Report results
    elapsed = time.time() - start_time
    final_count = vectorstore._collection.count()

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)
    print(f"  Total vectors: {final_count:,}")
    print(f"  Total time: {elapsed:.1f} seconds")
    print(f"  Speed: {final_count / elapsed:.0f} vectors/second")
    print()
    print("EFFICIENCY STATS:")
    print(f"  - Original codes: {total_codes:,}")
    print(f"  - Optimized vectors: {final_count:,}")
    print(f"  - Compression ratio: {total_codes / final_count:.1f}x fewer vectors to search")
    print()
    print("[+] Ready for fast medical queries!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()
