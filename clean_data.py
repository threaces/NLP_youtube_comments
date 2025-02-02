import re
from connect_database import table
from pprint import pprint

x = table.scan()
comment_table = x['Items']

def clean_comment(comment: str) -> str:

    """
    Function to clean comment from emoticons etc.

    Args:
        comment (str); Raw comment collected from youtube
    Returns:
        comment (str); Cleaned comment from redudant elements f.e emoticons
    """

    comment = re.sub(r"@\w+", "", comment)

    comment = comment.lower()
    comment = re.sub(r"[^a-zA-Z0-9\s]", "", comment)
    comment = re.sub(r"\s+", " ", comment)

    return comment

list_of_modified_comments = []

for item in comment_table:
    original_comment = item['Comment']
    modified_comment = clean_comment(original_comment)
    item['Cleaned comment'] = modified_comment
    list_of_modified_comments.append(item)
    

pprint(list_of_modified_comments)