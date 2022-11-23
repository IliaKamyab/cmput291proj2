import pymongo
from load_json import load


def add_article():
    ids = []
    in_file, port = 'dblp-ref-10.json', 27017
    db = load(in_file, port)
    mycol = db["dblp"]
    for x in mycol.find({}, {"id": 1}):
        ids.append(x["id"])
    unique_id = input("Give a unique ID for this article: ")
    while unique_id in ids:
        unique_id = input(
            "Your given ID is not unique, give a unique ID for this article: ")
    authors = add_authors()
    title = input("Give a title for your article: ")
    year = int(input("Give a year for your article: "))
    article = {"id": unique_id, "title": title, "year": year, "authors": authors,
               "abstract": None, "venue": None, "references": [], "n_citation": 0}
    inserted = mycol.insert_one(article)


def add_authors():
    authors = []
    # number of elements as input
    n = int(input("Enter number of authors: "))

    # iterating till the range
    for i in range(0, n):
        author = (input("Enter author name: "))
        authors.append(author)
    return authors


def main():
    add_article()
    in_file, port = 'dblp-ref-10.json', 27017
    db = load(in_file, port)
    mycol = db["dblp"]
    for x in mycol.find({}, {"authors": 1, }):
        print(x)


main()
