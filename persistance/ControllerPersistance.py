
import pickle
import os

from model.User import User

directory = "data"

def generate_name_user_file(user: User):
    return generate_name_user_file_by_chatid(user.chat_id)
def generate_name_user_file_by_chatid(chat_id):
    return str(chat_id) + '.state_data.pickle'


def save_state_data(user: User):
    path = os.path.join(directory, generate_name_user_file(user))
    with open(path, 'wb') as handle:
        pickle.dump(user, handle)


def get_state_data(chatid: str) -> User:
    path = os.path.join(directory, generate_name_user_file_by_chatid(chatid))
    if not os.path.isfile(path):
        user = User(chatid, [])
        save_state_data(user)
        return user
    with open(path, 'rb') as handle:
        return pickle.load(handle)


def define_rule(hour, minute, msgrule, name_rule, chat_id):
    user = get_state_data(chat_id)
    user.add_rule(hour, minute, msgrule, name_rule)
    save_state_data(user)


def get_all_users() -> [User]:
    users = []
    for file in os.listdir(directory):
        f = os.path.join(directory, file)
        with open(f, 'rb') as handle:
            users.append(pickle.load(handle))
    return users
