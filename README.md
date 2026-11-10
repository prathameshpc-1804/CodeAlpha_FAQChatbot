# 🤖 CodeAlpha FAQ Chatbot

An interactive FAQ chatbot developed using Python, Natural Language Processing (NLP), TF-IDF vectorization, and cosine similarity. The chatbot understands user queries and retrieves the most relevant answers from a predefined FAQ dataset.

Built as part of the **CodeAlpha Artificial Intelligence Internship – Task 2**.

---

## 📌 Project Overview

The CodeAlpha FAQ Chatbot is designed to answer frequently asked questions related to Python programming and artificial intelligence.

It uses Natural Language Processing techniques to preprocess user queries and compare them with questions stored in a CSV database. Using TF-IDF vectorization and cosine similarity, the chatbot identifies the most relevant FAQ and returns its corresponding answer.

The application provides an interactive interface built with Streamlit, allowing users to ask questions, select suggested questions, and explore relevant information.

---

## ✨ Features

- **Interactive Chat Interface:** User-friendly chatbot interface developed using Streamlit.
- **FAQ-Based Question Answering:** Retrieves answers from a predefined CSV dataset.
- **Natural Language Processing:** Processes text using tokenization, stopword removal, and lemmatization.
- **TF-IDF Vectorization:** Converts text into numerical vectors for comparison.
- **Cosine Similarity:** Identifies the most relevant FAQ based on similarity scores.
- **Suggested Questions:** Displays five randomly selected questions from the FAQ database.
- **Clickable Suggestions:** Users can click suggested questions to receive instant answers.
- **Refresh Suggestions:** Allows users to explore different questions.
- **Related Questions:** Includes functionality to retrieve questions similar to a given query.
- **Chat History:** Maintains conversation messages during the session.
- **Matching Details:** Displays the matched FAQ and similarity score.
- **Clear Conversation:** Allows users to reset the chat.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| NLTK | Natural Language Processing |
| Pandas | FAQ dataset management |
| Scikit-learn | TF-IDF and cosine similarity |
| CSV | FAQ data storage |

---

## 📂 Project Structure

```text
CodeAlpha_FAQChatbot/
│
├── app.py              # Streamlit application interface
├── chatbot.py          # FAQ matching and chatbot logic
├── preprocessing.py    # Text preprocessing using NLTK
├── faqs.csv            # FAQ questions and answers
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
├── .gitignore          # Files excluded from Git
│
└── .venv/              # Python virtual environment (not uploaded)
```

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_FAQChatbot.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Navigate to the Project Directory

```bash
cd CodeAlpha_FAQChatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Download Required NLTK Resources

Open Python in your terminal:

```bash
python
```

Execute:

```python
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
```

Then exit Python:

```python
exit()
```

### 7. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your default web browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

## 🧠 How It Works

The chatbot follows these steps to process and answer user queries:

**1. User Input**

The user enters a question through the Streamlit chat interface or selects one of the suggested questions.

**2. Text Preprocessing**

The input question is processed using NLTK techniques, including lowercasing, punctuation removal, tokenization, stopword removal, and lemmatization.

**3. TF-IDF Vectorization**

The processed question is converted into a numerical vector using TF-IDF (Term Frequency–Inverse Document Frequency).

**4. Similarity Calculation**

Cosine similarity calculates how closely the user's question matches the questions stored in the FAQ dataset.

**5. Best Match Selection**

The chatbot identifies the FAQ question with the highest similarity score.

**6. Answer Retrieval**

If the similarity score meets the configured threshold, the corresponding answer is retrieved from the CSV dataset.

**7. Response Display**

The chatbot displays the answer along with matching details. If no suitable match is found, it asks the user to rephrase the question.

---

## 📊 FAQ Dataset

The chatbot uses a CSV file named `faqs.csv` containing two columns:

| Column | Description |
|---|---|
| question | Frequently asked question |
| answer | Corresponding answer |

The dataset contains questions covering programming concepts and related technical topics.

---

## 🚀 Future Enhancements

- Integration with generative AI models for more detailed responses.
- Improved semantic search using sentence embeddings.
- User feedback system for evaluating answer quality.
- Database integration for dynamically managing FAQs.
- Support for multiple programming languages.
- Improved context-aware conversations.

---

## 👨‍💻 Author

**YOUR NAME**

BSc Computer Science Graduate

Developed as part of the **CodeAlpha AI Internship – Task 2**.

---

## 📄 License

This project is developed for educational and internship purposes.