import string
import json
from collections import Counter
from docx import Document

def extract_and_count_words_from_docx(docx_path):
    # Load the Word document
    doc = Document(docx_path)

    # Counter for word occurrences
    word_counts = Counter()

    # Iterate through paragraphs in the document
    for paragraph in doc.paragraphs:
        # Split each paragraph into words
        words = paragraph.text.split()

        # Update the word counts
        word_counts.update(
            word.strip(string.punctuation).lower() for word in words if word.strip(string.punctuation)
        )

    return word_counts

def save_word_counts_to_file(word_counts, output_file):
    # Convert keys to strings before saving to JSON
    str_word_counts = {str(key): value for key, value in word_counts.items()}

    # Save the word counts to a JSON file
    with open(output_file, 'w') as file:
        json.dump(str_word_counts, file, indent=2)

def main():
    document_path = "C:/Users/Ben/Desktop/die Weiten/diary copy/copy of diary.docx"
    
    output_file = "C:/Users/Ben/Desktop/die Weiten/diary copy/stats.json"

    word_counts = extract_and_count_words_from_docx(document_path)

    save_word_counts_to_file(word_counts, output_file)
    print(f"Word counts saved to {output_file}")

if __name__ == "__main__":
    main()
