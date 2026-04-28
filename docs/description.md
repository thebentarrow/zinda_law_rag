You are tasked with building a lightweight question-and-answer (Q&A) web application that allows users to:
1. Ask questions based on a predefined set of legal FAQs
2. And receive AI-generated responses. output AI-generated responses.

The system should demonstrate retrieval-augmented generation (RAG) by:
1. Combining FAQ storage,
2. relevance-based retrieval,
3. and AI-based answer generation through a simple user interface.

## Objective
Design and implement a minimum viable product (MVP) that:
1. Stores a dataset of legal FAQs.
2. Retrieves the most relevant FAQs when a user submits a question.
3. Uses an AI model to generate a contextual answer.
4. Displays the answer clearly in a web interface.
5. Logs user questions and AI responses for later review.


## Technical Requirements
Backend: Any Python framework (FastAPI / Flask / Django)
Frontend: TypeScript-based UI
RAG: Use any vector database for FAQ retrieval
LLM: Any AI model (OpenAI preferred)
Infrastructure: Fully Dockerized
Code Management: Github

## Acceptance Criteria
• The system contains 50–100 legal FAQ question/answer pairs stored for retrieval.
• UI allows users to submit questions.
• The system retrieves the top 1–2 most relevant FAQs.
• Retrieved FAQs are used as context for AI answer generation.
• AI-generated responses are displayed clearly to the user.
• Retrieved FAQ titles or IDs are visible with the answer.
• User queries and AI responses are logged and viewable.