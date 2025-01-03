import csv
from rdflib import URIRef,Literal,Namespace,Graph
from rdflib.namespace import RDF,OWL

# Etape 1 : Importer le fichier via csv.reader

with open('ml-100k/u1.base', 'r') as csvfile:
    try:
        csv_reader = csv.reader(csvfile, delimiter="\t")
    except FileNotFoundError:
        print("Erreur fichier introuvable")
        exit(0)
    N = list(csv_reader)
    user_id,item_id,rating,timestamp = zip(*N)
    user_id = [ int(x) for x in user_id]
    item_id = [ int(x) for x in item_id]
    rating = [ int(x) for x in rating]
    #print(user_id)
    #print(item_id)
    #print(max(item_id))

    # Pour eviter de surcharger Protege, on va prendre un échantillon de 200 éléments, on ignore timestamp.

    user_id_sample = user_id[:200]
    item_id_sample = item_id[:200]
    rating_sample = rating[:200]



    # Define the namespace
    Movie_namespace = Namespace("http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#")

    # Create the graph
    g = Graph()
    g.parse("Movie.rdf")

    #Bind the namespace to ensure proper prefixes
    g.bind("Movie", Movie_namespace)

    # Create a new individual and add properties
    User2 = Movie_namespace.User2
    user_id = Literal(user_id_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    movieId = Literal(item_id_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    rating = Literal(rating_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")

    g.add((User2, RDF.type, OWL.NamedIndividual))  # Declare as NamedIndividual
    g.add((User2, RDF.type, Movie_namespace.Rating))
    g.add((User2, Movie_namespace.userId, user_id))
    g.add((User2, Movie_namespace.movieId, movieId))
    g.add((User2, Movie_namespace.rate, rating))

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


