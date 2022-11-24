from load_json import load

def get_input() -> int:
    venue_count = input("Provide the number of top venues to search for: ")
    is_valid_number = False
    while not is_valid_number:
        try:
            venue_count = int(venue_count)
            assert venue_count > 0
            is_valid_number = True
        except:
            venue_count = input("Not a positive integer. Try again: ")

    return venue_count

def get_top_venues(n: int, db):
    # sort venues by number of papers that have venue in references (references field -> list of objectIDs of papers)
    # get number of papers in venue (venue field)
    venues = db.dblp.aggregate([
        {
            "$group": { 
                "_id": "$venue", 
                "count": {"$sum": 1},
                "papers": {"$push": "$id"},
            }
        },
        {
            "$sort":{'count':-1}
        }
    ])

    return venues

def print_venues(venues: list) -> None:
    return

def list_venues() -> None:
    n = get_input()
    venues = get_top_venues()
    print_venues(venues)

if __name__ == "__main__":
    print(get_input())
    db = load('dblp-ref-10.json', 27017)
    venues = get_top_venues(10, db)
    for thing in venues:
        print(thing["_id"], "Refs:", thing["papers"])