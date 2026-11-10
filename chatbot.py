
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess_text


class FAQChatbot:
    """Find relevant answers and suggest questions from an FAQ dataset."""

    def __init__(self, faq_file="faqs.csv", threshold=0.20):
        self.threshold = threshold

        # --------------------------------------------------
        # 1. Load the FAQ dataset
        # --------------------------------------------------

        self.faqs = pd.read_csv(faq_file)

        # Validate the dataset structure.
        required_columns = {"question", "answer"}

        if not required_columns.issubset(self.faqs.columns):
            raise ValueError(
                "The CSV file must contain 'question' and 'answer' columns."
            )

        # Remove rows with missing questions or answers.
        self.faqs = self.faqs.dropna(
            subset=["question", "answer"]
        ).copy()

        # Convert questions and answers to strings.
        self.faqs["question"] = self.faqs["question"].astype(str)
        self.faqs["answer"] = self.faqs["answer"].astype(str)

        # Remove blank questions and answers.
        self.faqs = self.faqs[
            self.faqs["question"].str.strip().ne("")
            & self.faqs["answer"].str.strip().ne("")
        ].copy()

        if self.faqs.empty:
            raise ValueError(
                "The FAQ dataset contains no valid FAQ entries."
            )

        # --------------------------------------------------
        # 2. Preprocess the FAQ questions
        # --------------------------------------------------

        self.faqs["processed_question"] = (
            self.faqs["question"].apply(preprocess_text)
        )

        # Remove questions that become empty after preprocessing.
        self.faqs = self.faqs[
            self.faqs["processed_question"].apply(
                lambda text: (
                    isinstance(text, str) and bool(text.strip())
                )
            )
        ].copy()

        if self.faqs.empty:
            raise ValueError(
                "No FAQ questions contain meaningful words after preprocessing."
            )

        # --------------------------------------------------
        # 3. Make questions available to the Streamlit app
        # --------------------------------------------------

        # The app uses this list to display suggested questions.
        self.questions = self.faqs["question"].tolist()

        # --------------------------------------------------
        # 4. Build the TF-IDF model
        # --------------------------------------------------

        self.vectorizer = TfidfVectorizer()

        try:
            self.faq_vectors = self.vectorizer.fit_transform(
                self.faqs["processed_question"]
            )

        except ValueError as exc:
            raise ValueError(
                "Could not build the TF-IDF model. "
                "Check your FAQ questions and preprocessing function."
            ) from exc

    # --------------------------------------------------
    # 5. Find an answer to a user's question
    # --------------------------------------------------

    def get_answer(self, user_question):
        """Return the best-matching answer and similarity score."""

        if (
            not isinstance(user_question, str)
            or not user_question.strip()
        ):
            return {
                "answer": "Please enter a question.",
                "matched_question": None,
                "similarity": 0.0,
                "found": False,
            }

        # Preprocess the user's question.
        processed_question = preprocess_text(user_question)

        if not isinstance(processed_question, str):
            processed_question = ""

        if not processed_question.strip():
            return {
                "answer": (
                    "I couldn't identify meaningful words in your question. "
                    "Please try asking in a different way."
                ),
                "matched_question": None,
                "similarity": 0.0,
                "found": False,
            }

        # Convert the question into a TF-IDF vector.
        question_vector = self.vectorizer.transform(
            [processed_question]
        )

        # Handle questions containing only words absent from the FAQ data.
        if question_vector.nnz == 0:
            return {
                "answer": (
                    "Sorry, I couldn't find a suitable answer. "
                    "Please try rephrasing your question."
                ),
                "matched_question": None,
                "similarity": 0.0,
                "found": False,
            }

        # Calculate similarity against stored FAQ questions.
        similarity_scores = cosine_similarity(
            question_vector,
            self.faq_vectors
        ).flatten()

        # Find the highest-scoring FAQ.
        best_index = similarity_scores.argmax()
        best_score = float(similarity_scores[best_index])

        # Reject weak matches.
        if best_score < self.threshold:
            return {
                "answer": (
                    "Sorry, I couldn't find a suitable answer. "
                    "Please try rephrasing your question or asking "
                    "about a topic covered by the FAQs."
                ),
                "matched_question": None,
                "similarity": best_score,
                "found": False,
            }

        return {
            "answer": self.faqs.iloc[best_index]["answer"],
            "matched_question": self.faqs.iloc[best_index]["question"],
            "similarity": best_score,
            "found": True,
        }

    # --------------------------------------------------
    # 6. Find related questions
    # --------------------------------------------------

    def get_related_questions(
        self,
        user_question,
        number=4,
        exclude_question=None
    ):
        """
        Return FAQ questions most similar to the user's question.

        This method can be used to display related questions
        beneath an answer in the Streamlit interface.
        """

        if (
            not isinstance(user_question, str)
            or not user_question.strip()
        ):
            return []

        # Preprocess the user's question.
        processed_question = preprocess_text(user_question)

        if (
            not isinstance(processed_question, str)
            or not processed_question.strip()
        ):
            return []

        # Convert the question into a TF-IDF vector.
        question_vector = self.vectorizer.transform(
            [processed_question]
        )

        if question_vector.nnz == 0:
            return []

        # Compare the question with every stored FAQ question.
        similarity_scores = cosine_similarity(
            question_vector,
            self.faq_vectors
        ).flatten()

        # Examine the highest-scoring questions first.
        ranked_indices = similarity_scores.argsort()[::-1]

        related_questions = []

        for index in ranked_indices:
            question = self.faqs.iloc[index]["question"]
            score = float(similarity_scores[index])

            # Do not recommend the same question.
            if question.strip().casefold() == user_question.strip().casefold():
                continue

            # Exclude the FAQ that already answered the question.
            if (
                exclude_question is not None
                and question.strip().casefold()
                == exclude_question.strip().casefold()
            ):
                continue

            # Avoid displaying unrelated suggestions.
            if score < 0.05:
                continue

            related_questions.append(question)

            if len(related_questions) >= number:
                break

        return related_questions


# --------------------------------------------------
# 7. Test the chatbot when this file is executed directly
# --------------------------------------------------

if __name__ == "__main__":

    try:
        chatbot = FAQChatbot("faqs.csv")

        print("Total FAQs loaded:", len(chatbot.questions))

        print("\nSample suggested questions:")

        for question in chatbot.questions[:5]:
            print("-", question)

        test_questions = [
            "What is Python?",
            "How do I create a function?",
            "Explain the difference between a list and a tuple.",
            "What is machine learning?",
            "How can I travel to the moon?",
        ]

        for question in test_questions:

            result = chatbot.get_answer(question)

            print("\nUser question:", question)
            print("Matched FAQ:", result["matched_question"])
            print("Similarity:", round(result["similarity"], 3))
            print("Found:", result["found"])
            print("Answer:", result["answer"])

            if result["found"]:
                related = chatbot.get_related_questions(
                    question,
                    number=3,
                    exclude_question=result["matched_question"]
                )

                print("Related questions:", related)

    except FileNotFoundError:
        print("Error: faqs.csv was not found.")

    except ImportError:
        print(
            "Error: Could not import preprocessing.py or "
            "one of its required dependencies."
        )

    except ValueError as exc:
        print("Configuration error:", exc)
