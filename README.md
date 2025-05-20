# AI Chat Log Summarizer

A Python tool that analyzes chat logs between users and AI, providing statistics and keywords.

## Features

- Parses chat logs with User/AI messages
- Provides message statistics (number of message exchanged)
- Extracts most common keywords using Tf-IDf
- Generates conversation summary
- Summary processing of multiple files

## Requirements

- Python 3.7+
- Libraries: nltk, scikit-learn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hasibul006/AI-Chat-Log-Summarizer.git
   cd AI-Chat-Log-Summarizer
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Give this command on powershell
```bash
python .\chat_summarizer.py
```

## Sample input

```
User: Hello!
AI: Hi! How can I assist you today?
User: Can you explain what machine learning is?
AI: Certainly! Machine learning is a field of AI that allows systems to learn from data.
User: What programming languages are used in machine learning?
AI: Python is the most popular language for machine learning.
```

## Sample Output
Two separate text files will be generated for single file and multiple file summary.
The sample of single file summary:
```
Summary of a single file:
    - The conversation had 6 exchanges.
    - The user asked mainly about learning, machine.
    - Most common keywords: learning, machine, hello.
```


##  TF-IDF Explanation

**TF-IDF (Term Frequency–Inverse Document Frequency)** is a statistical method used to find the most important words in a set of documents or text data.


### TF-IDF Calculation

1. **Term Frequency (TF)**  
   Measures how frequently a word appears in a document.

   ```
   TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
   ```

2. **Inverse Document Frequency (IDF)**  
   Measures how rare a word is across all documents.

   ```
   IDF(t) = log(Total number of documents / Number of documents containing term t)
   ```

3. **TF-IDF Score**  
   The final score:

   ```
   TF-IDF(t) = TF(t) × IDF(t)
   ```


### Why TF-IDF?

- **High TF-IDF score**: The word is frequent in a document but rare in others — it likely carries important meaning.
- **Low TF-IDF score**: The word is common across many documents (like "the", "is") and is probably not significant.


### Usage in This Project

In this project, we use TF-IDF to:
- Analyze user and AI messages in text chat files.
- Extract **top keywords** and summarize the **main topics** discussed.
- Identify what's important based on the **frequency and uniqueness** of words.

This helps create a concise summary of the conversation contents.

