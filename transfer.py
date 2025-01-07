import csv
from rdflib import URIRef,Literal,Namespace,Graph
from rdflib.namespace import RDF,OWL


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
    #print(N_sample)

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
    #print(N3)

with open('ml-100k/u.user','r') as csvfile4:
    try:
        csv_reader = csv.reader(csvfile4,delimiter='|')
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N4 = list(csv_reader)
    #print(N4)

with open('ml-100k/u.occupation','r') as csvfile5:
    try:
        csv_reader = csv.reader(csvfile5)
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N5 = list(csv_reader)
    #print(N5)


#Etape 2 : Ecrire les instances sous forme RDF/XML

    # Define the namespace
    Movie_namespace = Namespace("http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#")

    # Create the graph
    g = Graph()
    g.parse("Movie.rdf")

    #Bind the namespace to ensure proper prefixes
    g.bind("Movie", Movie_namespace)


    # Create a new individual and add properties
    for i in range(len(N_sample)):
        User = Movie_namespace[f"User{i}"]
        user_id = Movie_namespace[f"User{N_sample[i][0]}"]
        movie_id = Movie_namespace[f"Movie{N_sample[i][1]}"]
        rating = Literal(N_sample[i][2], datatype="http://www.w3.org/2001/XMLSchema#decimal")

        g.add((User, RDF.type, OWL.NamedIndividual))  # Declare as NamedIndividual
        g.add((User, RDF.type, Movie_namespace.Rating))
        g.add((User, Movie_namespace.hasForUser, user_id))
        g.add((User, Movie_namespace.hasForMovie, movie_id))
        g.add((User, Movie_namespace.rate, rating))

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


