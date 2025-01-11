import csv
from rdflib import URIRef,Literal,Namespace,Graph
from rdflib.namespace import RDF,OWL
from datetime import datetime

# Etape 1 : Importer tous les fichier via csv.reader

with open('ml-100k/u1.base', 'r') as csvfile1:
    try:
        csv_reader = csv.reader(csvfile1, delimiter="\t")
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N1 = list(csv_reader)
    # Pour eviter de surcharger Protege, on va prendre un échantillon de 200 éléments, on ignore timestamp.

    N_sample = N1[:200]
    N_sample = [ x[:3] for x in N_sample ] #Removing the timestamp 
    print(N_sample)

with open('ml-100k/u.genre','r') as csvfile2:
    try:
        csv_reader = csv.reader(csvfile2,delimiter='|')
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N2 = list(csv_reader)
    #print(N2)

with open('ml-100k/u.item','r', encoding='ISO-8859-1') as csvfile3:
    try:
        csv_reader = csv.reader(csvfile3,delimiter='|')
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N3 = list(csv_reader)
    #N3 = [ k for (....) ]
    #print(N3)

with open('ml-100k/u.user','r') as csvfile4:
    try:
        csv_reader = csv.reader(csvfile4,delimiter='|')
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N4 = list(csv_reader)
    #print(N4)
    

    #Etape 2 : Ecrire les instances sous forme RDF/XML

    # Define the namespace
    Movie_namespace = Namespace("http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#")

    # Create the graph
    g = Graph()
    g.parse("Movie.rdf")

    #Bind the namespace to ensure proper prefixes
    g.bind("Movie", Movie_namespace)


    #User
    for i in range(len(N4)):
        User = Movie_namespace[f"User{i}"]
        user_id = Literal(int(N4[i][0]), datatype="http://www.w3.org/2001/XMLSchema#int")
        age = Literal(int(N4[i][1]), datatype="http://www.w3.org/2001/XMLSchema#int")
        user_gender = Literal(N4[i][2], datatype="http://www.w3.org/2001/XMLSc/hema#string")
        occupation = Literal(N4[i][3], datatype="http://www.w3.org/2001/XMLSchema#string")
        zipcode = Literal(N4[i][4], datatype="http://www.w3.org/2001/XMLSchema#string")

        g.add((User, RDF.type, OWL.NamedIndividual))
        g.add((User, RDF.type, Movie_namespace.User))
        g.add((User, Movie_namespace.userId, user_id))
        g.add((User, Movie_namespace.age, age))
        g.add((User, Movie_namespace.gender, user_gender))
        g.add((User, Movie_namespace.occupation, occupation))
        g.add((User, Movie_namespace.zipcode, zipcode))        
   

    #Kind - Les genres du film 
    for i in range (len(N2)):
        Kind = Movie_namespace[f"Kind{i}"]
        kind_id = Literal(i, datatype="http://www.w3.org/2001/XMLSchema#int")
        kind_name = Literal(N2[i][0], datatype="http://www.w3.org/2001/XMLSchema#string")
        #print(kind_name)
        g.add((Kind, RDF.type, OWL.NamedIndividual))
        g.add((Kind, RDF.type, Movie_namespace.Kind))
        g.add((Kind, Movie_namespace.kindId, kind_id))
        g.add((Kind, Movie_namespace.kind, kind_name))

    # Movie Class
    for i in range(len(N3)):
        Movie = Movie_namespace[f"Movie{i}"]
        movie_id = Literal(N3[i][0], datatype="http://www.w3.org/2001/XMLSchema#decimal")
        title = Literal(N3[i][1], datatype="http://www.w3.org/2001/XMLSchema#string")
        imdb_url = Literal(N3[i][4], datatype="http://www.w3.org/2001/XMLSchema#string")

        try:
            #print(f"Movie : {movie_id} | Date : {N3[i][2]}")
            if N3[i][2].strip():
                release_date_value = datetime.strptime(N3[i][2],"%d-%b-%Y").strftime("%Y-%m-%dT00:00:00") # On converti la chaine de caractère en temps 
                release_date = Literal(release_date_value, datatype="http://www.w3.org/2001/XMLSchema#dateTime")
            else:
                raise ValueError(f"Warning : Adding a movie {movie_id} without a release date")
        except ValueError as e:
            print(f"Error while parsing: {e}")
            release_date = Literal(release_date_value, datatype="http://www.w3.org/2001/XMLSchema#dateTime")
            #exit(1)
        
        g.add((Movie, RDF.type, OWL.NamedIndividual))
        g.add((Movie, RDF.type, Movie_namespace.Movie))
        g.add((Movie, Movie_namespace.movieId, movie_id))
        g.add((Movie, Movie_namespace.movieTitle, title))
        g.add((Movie, Movie_namespace.releaseDate, release_date))
        g.add((Movie, Movie_namespace.IMDbUrl, imdb_url))

        # Add Object Property for kinds
        for j in range(5, 23):
            if N3[i][j] == '1':  # Movie belongs to this kind
                kind_ref = Movie_namespace[f"Kind{j - 5}"]
                g.add((Movie, Movie_namespace.hasForKind, kind_ref))



    #Rating
    for i in range(len(N_sample)):
        Item = Movie_namespace[f"Item{i}"]
        item_id = Literal(i,datatype="http://www.w3.org/2001/XMLSchema#int")
        user_id = Movie_namespace[f"User{N_sample[i][0]}"]
        movie_id = Movie_namespace[f"Movie{N_sample[i][1]}"]
        rating = Literal(int(N_sample[i][2]), datatype="http://www.w3.org/2001/XMLSchema#int")

        g.add((Item, RDF.type, OWL.NamedIndividual))  # Declare as NamedIndividual
        g.add((Item, RDF.type, Movie_namespace.Rating))
        g.add((Item,Movie_namespace.itemId,item_id))
        g.add((Item, Movie_namespace.hasForUser, user_id))
        g.add((Item, Movie_namespace.hasForMovie, movie_id))
        g.add((Item, Movie_namespace.rate, rating))

    """
    Item2 = Movie_namespace.Item2
    #user_id = Movie_namespace[f"User{N_sample[1][0]}"]
    user_id = Literal(N_sample[1][0], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    movie_id = Movie_namespace[f"Movie{N_sample[1][1]}"]
    #movieId = Literal(item_id_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    rating = Literal(N_sample[1][2], datatype="http://www.w3.org/2001/XMLSchema#decimal")

    g.add((Item2, RDF.type, OWL.NamedIndividual))  # Declare as NamedIndividual
    g.add((Item2, RDF.type, Movie_namespace.Rating))
    g.add((Item2, Movie_namespace.userId, user_id))
    g.add((Item2, Movie_namespace.hasForMovie, movie_id))
    g.add((Item2, Movie_namespace.rate, rating))
    """

    RDF_file = g.serialize(format='xml')
    #print(RDF_file)

    # Write to file
    with open("New_Movie.rdf", 'w', encoding='utf-8') as rdf_output:
        rdf_output.write(RDF_file)

    print(f"RDF data successfully written")

    """
    for i in range(0,20):
        print(N1[i])
        print(N2[i])
        print(N3[i])
        print(N4[i])
    """


"""
with open('ml-100k/u.occupation','r') as csvfile5:
    try:
        csv_reader = csv.reader(csvfile5)
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N5 = list(csv_reader)
    #print(N5)
"""


