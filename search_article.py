import re
from load_json import load 


def article_search(db):
    keywords = input("Enter keywords: ").split(" ")
    
    int_list = []
    for keyword in keywords:
        if keyword.isdigit():
            int_list.append(int(keyword))

    lst = keywords
    #dblp = db["dblp"]
    articles = db.dblp.find({"$or":[{"abstract":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"title":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"authors":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"venue":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"year":{"$in":int_list}}]},{"references":0,"n_citation":0,"references":0,"authors":0,"abstract":0,"_id":0})
    return articles

def select_article(db, aid):
    #dblp = db["dblp"]
    article = db.dblp.find({"id":aid},{"references":0,"n_citation":0,"references":0,"_id":0})
    article = article[0]
    result = ', '.join(f'{key}: {value}' for key, value in article.items())
    print(result)

    return article

def article_selection(db, aid, a_dict):
    choice = input("Select article: ")
    try:
        aid = a_dict[int(choice)]
        article = select_article(db, aid)
        articles = referencing_articles(db, aid)
    except:
        print("Invalid choice")

def referencing_articles(db, aid):
    #dblp = db["dblp"]
    print("Articles that reference chosen article:")
    articles = db.dblp.find({"references":re.compile(aid)},{"id":1,"title":1,"year":1,"_id":0})

    for article in articles:
        result = ', '.join(f'{key}: {value}' for key, value in article.items())
        print(result)
        
    return articles

def article_display(articles):
    i = 1
    article_dict = {}
    for article in articles:
        result = ', '.join(f'{key}: {value}' for key, value in article.items())
        print(str(i)+".",result)
        article_dict[i] = article["id"]
        i += 1
    return article_dict
    

def main():
    #in_file = input("Enter a file for data input:")
    #port = input("Enter a port number:")
    in_file,port = 'dblp-ref-10.json', 27017
    db = load(in_file, port)
    articles = article_search(db)
    a_dict = article_display(articles)
    article_selection(db, articles, a_dict)

    

main()





    
