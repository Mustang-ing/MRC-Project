import csv
from rdflib import URIRef,Literal,Namespace,Graph
from rdflib.namespace import RDF

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

    g = Graph() # Generation d'un objet RDF Graphe (Ontologie)
    g.parse("Movie.rdf")
    # print(g.serialize()) POur voir si l'ontologie est bien charger
    #Objectif : Générer un nouvel inidividu prenant pour informations la 2eme ligne du data csv 

    #Commencer par faire le namespace
    
    Movie_namespace = Namespace("http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl")
    
    User2 = n.User2 # http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl/User2
    user_id = Literal(user_id_sample[1])
    movieId = Literal(item_id_sample[1])
    rating = Literal(rating_sample[1])

    print(f"User2 : URI : {User2} | User_id : {user_id} | MovieId : {movieId} | Rating : {rating}")
    
    g.add((User2,RDF.type,n.Rating) #Ajouter le triplet sur le type
    g.add((User2,n.userId,user_id))  
    g.add((User2,n.movieid,movieId))
    g.add((User,n.rate,rate))

    print(g.serialize())


    """
    for i in range(0,20):
        print(N1[i])
        print(N2[i])
        print(N3[i])
        print(N4[i])
    """


