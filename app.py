import re
from load_json import load 
from add_article import add_article
from list_venues import list_venues

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

def article_selection(db, a_dict):
    
    choice = input("1.Select article\n2.Main menu\n")
    if choice == "1":
        article_choice = input("Select article: ")
        try:
            aid = a_dict[int(article_choice)]
        except:
            print("Invalid choice")
            article_selection(db, a_dict)
        else:
            select_article(db, aid)
            referencing_articles(db, aid)
            main_screen(db)


    elif choice == "2":
        main_screen(db)
    

def referencing_articles(db, aid):
    #dblp = db["dblp"]
    print("Articles that reference chosen article:")
    articles = db.dblp.find({"references":re.compile(aid)},{"id":1,"title":1,"year":1,"_id":0})

    for article in articles:
        result = ', '.join(f'{key}: {value}' for key, value in article.items())
        print(result)
        


def article_display(articles):
    i = 1
    article_dict = {}
    for article in articles:
        result = ', '.join(f'{key}: {value}' for key, value in article.items())
        print(str(i)+".",result)
        article_dict[i] = article["id"]
        i += 1
    return article_dict




def article_search_all(db):
    articles = article_search(db)
    a_dict = article_display(articles)
    article_selection(db, a_dict)






"""--------------------------------------------------------------------------------------------"""

def author_search(db):
    keywords = input("Enter keywords: ").split(" ")
    
    lst = keywords
    #dblp = db["dblp"]
    articles = db.dblp.aggregate([{"$unwind":"$authors"},{"$match": {"authors":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}}},{"$group": {"_id":"$authors","count":{"$sum": 1}}}   ])
    i = 1
    author_dict = {}
    for article in articles:
        result = ', '.join(f' {value}' for key, value in article.items())
        print(str(i)+".",result)
        author_dict[i] = article["_id"]
        i += 1    
    return author_dict

def get_articles_by_author(db,author):
    articles = db.dblp.find({"authors":re.compile(author, re.IGNORECASE)},{"title":1,"year":1,"venue":1,"_id":0}).sort("year",-1)
    for article in articles:
        result = ', '.join(f'{key}: {value}' for key, value in article.items())
        print(result)
    


def author_search_all(db):
    a_dict = author_search(db)
    author_selection(db, a_dict)

def author_selection(db, a_dict):
    choice = input("1.Select author\n2.Main menu\n")
    if choice == "1":
        author_choice = input("Select author: ")
        try:
            author = a_dict[int(author_choice)]
            
        except:
            print("Invalid choice")
            author_selection(db, a_dict)
        else:
            get_articles_by_author(db, author)
            main_screen(db)

    elif choice == "2":
        main_screen(db)
    
def main_screen(db):
    choice = input("1. Search for articles\n2. Search for authors\n3. Add Article\n4. Exit\n")
    if choice == "1":
        article_search_all(db)
    elif choice == "2":
        author_search_all(db)
    elif choice == "3":
        add_article(db)
        main_screen(db)
    elif choice =="4":
        print("Exiting...")
        quit()
    else:
        print("Invalid choice")
        main_screen(db)


def add_article(db):
    aid = input("Enter article id: ")
    count = db.dblp.count_documents({"id":aid})
    if count >0:
        print("Article with id already exists")
        add_article(db)
        return
    authors = input("Enter authors: ").split(",")
    print(authors)
    title = input("Enter title: ")
    year = int(input("Enter year: "))
    new_article = {"id":aid,"title":title,"authors":authors,"year":year,"n_citation":0,"references":[],"venue":None,"abstract":None}
    db.dblp.insert_one(new_article)


if __name__ == "__main__":
    #in_file = input("Enter a file for data input:")
    #port = input("Enter a port number:")
    in_file,port = 'dblp-ref-10.json', 27017
    db = load(in_file, port)
    
    main_screen(db)
    #add_article(db,"1234","test1",["author11","author12"],2020)
    #add_article(db,"1234","test2",["author21","author22"],2020)