
import csv
import random
from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, OWL, XSD
from datetime import datetime

Taille_sample = 500  # Nombre de lignes (de Rating) à extraire

# Etape 1 : Importer tous les fichiers via csv.reader
try:
    with open('ml-100k/u1.base', 'r') as csvfile1:
        csv_reader = csv.reader(csvfile1, delimiter="\t")
        N1 = list(csv_reader)
except FileNotFoundError:
    print("Erreur : fichier 'u1.base' introuvable.")
    exit(1)

try:
    with open('ml-100k/u.genre', 'r') as csvfile2:
        csv_reader = csv.reader(csvfile2, delimiter='|')
        N2 = list(csv_reader)
except FileNotFoundError:
    print("Erreur : fichier 'u.genre' introuvable.")
    exit(1)

try:
    with open('ml-100k/u.item', 'r', encoding='ISO-8859-1') as csvfile3:
        csv_reader = csv.reader(csvfile3, delimiter='|')
        N3 = list(csv_reader)
except FileNotFoundError:
    print("Erreur : fichier 'u.item' introuvable.")
    exit(1)

try:
    with open('ml-100k/u.user', 'r') as csvfile4:
        csv_reader = csv.reader(csvfile4, delimiter='|')
        N4 = list(csv_reader)
except FileNotFoundError:
    print("Erreur : fichier 'u.user' introuvable.")
    exit(1)

# Sélection aléatoire de Taille_sample lignes
N_sample = random.sample(N1, Taille_sample)

N_sample = [x[:3] for x in N_sample]  # Suppression de la colonne timestamp

# Extraire les utilisateurs et les films des 200 lignes
selected_users = {x[0] for x in N_sample}
selected_movies = {x[1] for x in N_sample}

# Etape 2 : Ecrire les instances sous forme RDF/XML
Movie_namespace = Namespace("http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#")

g = Graph()
try:
    g.parse("Movie.rdf")
except FileNotFoundError:
    print("Erreur : fichier 'Movie.rdf' introuvable.")
    exit(1)

# Bind namespace
g.bind("Movie", Movie_namespace)

# Ajout des utilisateurs sélectionnés
for user in N4:
    if user[0] in selected_users:
        user_uri = Movie_namespace[f"User{user[0]}"]
        g.add((user_uri, RDF.type, OWL.NamedIndividual))
        g.add((user_uri, RDF.type, Movie_namespace.User))
        g.add((user_uri, Movie_namespace.userId, Literal(int(user[0]), datatype=XSD.int)))
        g.add((user_uri, Movie_namespace.age, Literal(int(user[1]), datatype=XSD.int)))
        g.add((user_uri, Movie_namespace.gender, Literal(user[2], datatype=XSD.string)))
        g.add((user_uri, Movie_namespace.occupation, Literal(user[3], datatype=XSD.string)))
        g.add((user_uri, Movie_namespace.zipcode, Literal(user[4], datatype=XSD.string)))

# Ajout des genres
for idx, genre in enumerate(N2):
    genre_uri = Movie_namespace[f"Kind{idx}"]
    g.add((genre_uri, RDF.type, OWL.NamedIndividual))
    g.add((genre_uri, RDF.type, Movie_namespace.Kind))
    g.add((genre_uri, Movie_namespace.kindId, Literal(idx, datatype=XSD.int)))
    g.add((genre_uri, Movie_namespace.kind, Literal(genre[0], datatype=XSD.string)))

# Ajout des films sélectionnés
for movie in N3:
    if movie[0] in selected_movies:
        movie_uri = Movie_namespace[f"Movie{movie[0]}"]
        g.add((movie_uri, RDF.type, OWL.NamedIndividual))
        g.add((movie_uri, RDF.type, Movie_namespace.Movie))
        g.add((movie_uri, Movie_namespace.movieId, Literal(movie[0], datatype=XSD.int)))
        g.add((movie_uri, Movie_namespace.movieTitle, Literal(movie[1], datatype=XSD.string)))
        
        if movie[2].strip():
            try:
                release_date = datetime.strptime(movie[2], "%d-%b-%Y").strftime("%Y-%m-%dT00:00:00")
                g.add((movie_uri, Movie_namespace.releaseDate, Literal(release_date, datatype=XSD.dateTime)))
            except ValueError:
                print(f"Erreur de conversion de la date pour le film {movie[0]}.")

        g.add((movie_uri, Movie_namespace.IMDbUrl, Literal(movie[4], datatype=XSD.string)))

        for j in range(5, 23):
            if movie[j] == '1':
                genre_uri = Movie_namespace[f"Kind{j - 5}"]
                g.add((movie_uri, Movie_namespace.hasForKind, genre_uri))

# Ajout des notations
for idx, sample in enumerate(N_sample):
    rating_uri = Movie_namespace[f"Rating{idx}"]
    user_uri = Movie_namespace[f"User{sample[0]}"]
    movie_uri = Movie_namespace[f"Movie{sample[1]}"]
    
    g.add((rating_uri, RDF.type, OWL.NamedIndividual))
    g.add((rating_uri, RDF.type, Movie_namespace.Rating))
    g.add((rating_uri, Movie_namespace.itemId, Literal(idx, datatype=XSD.int)))
    g.add((rating_uri, Movie_namespace.hasForUser, user_uri))
    g.add((rating_uri, Movie_namespace.hasForMovie, movie_uri))
    g.add((rating_uri, Movie_namespace.rate, Literal(int(sample[2]), datatype=XSD.int)))

# Sérialisation du graphe RDF
output_file = "New_Movie.rdf"
g.serialize(destination=output_file, format='xml')
print(f"RDF data successfully written to {output_file}")
