
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download the required NLTK resources
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Initialize stopwords and lemmatizer
STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def preprocess_text(text):
    """
    Clean and preprocess text for FAQ question matching.

    Steps:
    1. Convert text to lowercase.
    2. Remove punctuation and special characters.
    3. Tokenize the text into words.
    4. Remove common stopwords.
    5. Lemmatize words to their base forms.
    """
    # Handle invalid input
    if not isinstance(text, str):
        return ""

    # Convert text to lowercase
    text = text.lower()

    # Keep alphabetic characters and whitespace
    text = re.sub(r"[^a-z\s]", " ", text)

    # Tokenize the text into individual words
    tokens = nltk.word_tokenize(text, preserve_line=True)

    # Remove stopwords and lemmatize the remaining tokens
    processed_tokens = [
        LEMMATIZER.lemmatize(token)
        for token in tokens
        if token not in STOP_WORDS and len(token) > 1
    ]

    return " ".join(processed_tokens)


# Example usage
if __name__ == "__main__":
    sample_text = "What are the benefits of using Python for programming?"
    result = preprocess_text(sample_text)
    print("Original text:", sample_text)
    print("Preprocessed text:", result)
