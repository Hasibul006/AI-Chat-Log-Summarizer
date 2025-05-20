import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import os

def parsing_Messages(file_path):
    users_message = []
    ai_messages = []

    with open(file_path, 'r', encoding='utf-8') as chats:
        for line in chats:
            if line.startswith('User: '):
                users_message.append(line[6:].strip())
            elif line.startswith('AI: '):
                ai_messages.append(line[4:].strip())

    return users_message, ai_messages


def get_common_words(messages, top_n=5):
    stop_words = set(stopwords.words('english'))
    words = []

    for msg in messages:
        tokens = word_tokenize(msg.lower())
        words.extend([word for word in tokens if word.isalpha() and word not in stop_words])

    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def generate_summary(filepath):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    users_message, ai_messages = parsing_Messages(filepath)
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages
    common_words = get_common_words(users_message + ai_messages)

    topics = [word for word, _ in common_words[:3]]

    summary = f"""
========== Chat Summary ==========
Topics (Top 3): {', '.join(topics)}
Total messages: {num_total_messages}
User messages: {num_user_messages}
AI messages: {num_ai_messages}

Top {len(common_words)} Common Words:
""" + "\n".join([f"{word}: {count}" for word, count in common_words])

    print(summary)


if __name__ == '__main__':
    generate_summary("test_chat.txt")
