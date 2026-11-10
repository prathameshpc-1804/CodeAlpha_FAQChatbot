
import random
import streamlit as st
from chatbot import FAQChatbot


# --------------------------------------------------
# 1. Configure the Streamlit page
# --------------------------------------------------

st.set_page_config(
    page_title="CodeAlpha FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# 2. Application heading
# --------------------------------------------------

st.title("🤖 FAQ Chatbot")

st.markdown(
    """
    Welcome to the **CodeAlpha FAQ Chatbot**!

    Ask me questions about Python programming and
    artificial intelligence. You can type a question
    or select one of the suggested questions below.
    """
)

st.divider()


# --------------------------------------------------
# 3. Initialize the chatbot
# --------------------------------------------------

@st.cache_resource
def load_chatbot():
    """Load the FAQ chatbot and its TF-IDF model."""
    return FAQChatbot()


try:
    chatbot = load_chatbot()

except Exception as error:
    st.error(
        "Unable to load the chatbot. "
        "Please check your FAQ dataset and configuration."
    )

    st.exception(error)
    st.stop()


# --------------------------------------------------
# 4. Initialize conversation history
# --------------------------------------------------

WELCOME_MESSAGE = (
    "Hello! 👋 I'm your FAQ assistant. "
    "Ask me anything about Python programming!"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]


# --------------------------------------------------
# 5. Load suggested questions from the FAQ database
# --------------------------------------------------

if "suggested_questions" not in st.session_state:
    st.session_state.suggested_questions = random.sample(
        chatbot.questions,
        min(5, len(chatbot.questions))
    )


# --------------------------------------------------
# 6. Function to process a question
# --------------------------------------------------

def process_question(question):
    """Display and save a question and its FAQ answer."""

    # Display the user's question.
    with st.chat_message("user"):
        st.markdown(question)

    # Save the user's question.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Find the best answer.
    result = chatbot.get_answer(question)
    answer = result["answer"]

    # Display the chatbot's answer.
    with st.chat_message("assistant"):
        st.markdown(answer)

        with st.expander("View matching details"):
            if result["found"]:
                st.write(
                    "**Matched FAQ:**",
                    result["matched_question"]
                )

                st.write(
                    "**Similarity score:**",
                    f'{result["similarity"]:.3f}'
                )
            else:
                st.info(
                    "No sufficiently similar FAQ was found."
                )

    # Save the chatbot's answer.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# --------------------------------------------------
# 7. Display previous conversation messages
# --------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 8. Display clickable suggested questions
# --------------------------------------------------

st.subheader("💡 Suggested Questions")

st.caption(
    "Choose a question to get an answer instantly."
)

col1, col2 = st.columns(2)

for index, question in enumerate(
    st.session_state.suggested_questions
):
    # Arrange suggestions into two columns.
    column = col1 if index % 2 == 0 else col2

    with column:
        if st.button(
            question,
            key=f"suggested_question_{index}",
            use_container_width=True
        ):
            st.session_state.selected_question = question
            st.rerun()


# --------------------------------------------------
# 9. Refresh suggested questions
# --------------------------------------------------

if st.button("🔄 Show Other Questions"):
    st.session_state.suggested_questions = random.sample(
        chatbot.questions,
        min(5, len(chatbot.questions))
    )

    st.rerun()


# --------------------------------------------------
# 10. Accept typed or clicked questions
# --------------------------------------------------

typed_question = st.chat_input(
    "Type your question here..."
)

selected_question = st.session_state.pop(
    "selected_question",
    None
)

# Prioritize a clicked suggestion; otherwise use typed input.
user_question = selected_question or typed_question

if user_question:
    process_question(user_question)


# --------------------------------------------------
# 11. Sidebar information
# --------------------------------------------------

with st.sidebar:
    st.header("About")

    st.write(
        """
        This chatbot uses Natural Language Processing
        (NLP) to find relevant answers from a predefined
        FAQ dataset.
        """
    )

    st.subheader("Technologies")

    st.markdown(
        """
        - Python
        - Streamlit
        - NLTK
        - Pandas
        - Scikit-learn
        - TF-IDF
        - Cosine Similarity
        """
    )

    st.divider()

    st.caption("CodeAlpha Internship — Task 2")

    # Reset the conversation.
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }
        ]

        st.session_state.pop(
            "selected_question",
            None
        )

        st.rerun()
