from load_json import load

if __name__ == "__main__":    
    in_file = input("Enter a file for data input: ")
    port = input("Enter a port number: ")
    # in_file,port = 'dblp-ref-1m.json', "27017"
    load(in_file, port)