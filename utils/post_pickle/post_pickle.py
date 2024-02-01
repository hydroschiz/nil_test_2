import pickle


def save_post(post):
    with open("data/current_post.pickle", "wb") as f:
        pickle.dump(post, f)


def load_post():
    with open("data/current_post.pickle", "rb") as f:
        post = pickle.load(f)
    return post
