import argparse
import re
import json
import sys
from pathlib import Path

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

# Tokenizer (same logic as main.py)
def simple_tokenizer(text):
    return re.findall(r"\b\w+\b", text.lower())

def clean_and_tokenize(text):
    return set(simple_tokenizer(text))

def compare_keywords(resume_text, job_desc_text):
    resume_words = clean_and_tokenize(resume_text)
    job_keywords = clean_and_tokenize(job_desc_text)

    matched_keywords = resume_words & job_keywords
    missing_keywords = job_keywords - resume_words
    score = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0

    return round(score, 2), sorted(matched_keywords), sorted(missing_keywords)


def extract_text_from_pdf(path):
    if PyPDF2 is None:
        raise RuntimeError("PyPDF2 is not installed. Please install dependencies (pip install -r requirements.txt)")
    reader = PyPDF2.PdfReader(str(path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_text_file(path):
    return Path(path).read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="ATS Resume Checker (CLI)")
    # Make resume optional so we can prompt interactively instead of letting argparse error out
    parser.add_argument("--resume", "-r", required=False, help="Path to resume file (PDF or TXT)")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--job-file", "-jf", help="Path to a job description text file")
    group.add_argument("--job-text", "-jt", help="Job description text as a string (wrap in quotes)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # If resume wasn't provided on the command line, prompt the user interactively.
    if not args.resume:
        try:
            resume_input = input("Enter path to resume file (.pdf or .txt): ").strip()
        except EOFError:
            resume_input = ""
        if not resume_input:
            print("No resume provided. Use --resume or run interactively.")
            sys.exit(2)
        args.resume = resume_input

    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"Resume file not found: {resume_path}")
        sys.exit(2)

    # Read job description
    if args.job_text:
        job_desc = args.job_text
    elif args.job_file:
        job_file = Path(args.job_file)
        if not job_file.exists():
            print(f"Job file not found: {job_file}")
            sys.exit(2)
        job_desc = read_text_file(job_file)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("No job description provided. Use --job-text, --job-file, or pipe job description via stdin.")
            sys.exit(2)
        job_desc = sys.stdin.read()

    # Extract resume text
    suffix = resume_path.suffix.lower()
    if suffix == ".pdf":
        resume_text = extract_text_from_pdf(resume_path)
    elif suffix == ".txt":
        resume_text = read_text_file(resume_path)
    else:
        print("Unsupported resume format. Supported: .pdf, .txt")
        sys.exit(2)

    score, matched, missing = compare_keywords(resume_text, job_desc)

    result = {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ATS Match Score: {score}%")
        print("\nMatched keywords:")
        print(", ".join(matched) if matched else "None")
        print("\nMissing keywords:")
        print(", ".join(missing) if missing else "None")

if __name__ == "__main__":
    main()
