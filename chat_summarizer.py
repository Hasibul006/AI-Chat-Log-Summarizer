

def parsing_Messages(file_path):

    users_message = []
    ai_messages = []

    with open(file_path, 'r') as chats:
        for line in chats:
            if line.startswith('User: '):
                users_message.append(line[6:].strip())
            elif line.startswith('AI: '):
                ai_messages.append(line[4:].strip())

    return users_message, ai_messages


if __name__ == '__main__':
    users_message, ai_messages = parsing_Messages('test_chat.txt')
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages
    print("total num of messages: " + str(num_total_messages))
    print("num of user messages: " + str(num_user_messages))
    print("num of ai messages: " + str(num_ai_messages))
    print('\n' + "Users messages: ")
    for massage in users_message:
        print(massage)
    print('\n' + "AI messages: ")
    for massage in ai_messages:
        print(massage)

