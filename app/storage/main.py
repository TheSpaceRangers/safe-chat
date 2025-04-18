banned_topics: set[str] = set()

def load_optional_rules():
    banned_topics.update({
        "violences", "politics", "drugs"
    })