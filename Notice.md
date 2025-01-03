# Utilisation de RDFLib
La librairie RDFLib que j'au utiliser permet de générer un nouveau fichier RDF/XML voiçi les points clé à garder en tête :

## Objectif, matcher les informations dans Protege.
Dans Protege, j'ai pu générer un User1 assez facilement, cela à donner le code RDF/XML suivant :


    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#User1">
        <rdf:type rdf:resource="http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#Rating"/>
        <Movie:movieId rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">1</Movie:movieId>
        <Movie:rate rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">5</Movie:rate>
        <Movie:userId rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">1</Movie:userId>
    </owl:NamedIndividual>

## Librairie à utiliser 
from rdflib import URIRef,Literal,Namespace,Graph >> Permet d'utiliser les fonction principales
from rdflib.namespace import RDF,OWL >> Essentiel pour appeler des namespaces 

## Définir un namespace 

Un namespace permet de faire un alias afin d'éviter de mettre tout l'URI pour nommer un sujet. Içi l'URI qui va revenir le plus est celui de notre ontologie à savoir **"http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#"**

## Initialiser un graphe 
Un graphe permet de généré des triplet RDF, avant d'arriver à cette êtape là il faut réaliser deux actions essentiels 
  1) L'initialiser : **g = Graph()**
  2) Importer l'ontologie dans notre nouvel objet : **g.parse("Movie.rdf")** 
!!! **Attention : Je ne suis pas à ce stade de l'utilité de parser notre fichier de base**
  3) Associer l'URI au mot-clé "Movie" :  **g.bind("Movie", Movie_namespace)**

 ## Génération d'un individu
La encore, il faut utiliser plusieurs fonctions pour y arriver 
  - **Pour générer l'individu dans l'ontologie** : Il faut commencer par lui associer une URI, ça tombe bien on n'a déjà fait le travail avec le namespace : **User2 = Movie_namespace.User2** 
  Ce code est équivalent à ce dernier **User2 = URIRef(http://www.semanticweb.org/ing-mustang/ontologies/2024/11/Movie.owl#User2)**, si tu check dans l'ontologie générer dans Protege, tu vera que l'URI associè matche à la ligne 8 (Sauf pour owl:NamedIndividual)

## Ajout des data property 

On utilise la méthode Literal en précisant le datatype, sinon le type sera celui évalué par Python (c'est mal barré) : 
    user_id = Literal(user_id_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    movieId = Literal(item_id_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")
    rating = Literal(rating_sample[1], datatype="http://www.w3.org/2001/XMLSchema#decimal")

## Ajout des triplets RDF
Pour ajouter des triplets RDF dans l'ontologie, il faut utiliser add est précisé un tuple comme-ci : (Individu,Predicat,Ressorces)

 g.add((User2, RDF.type, OWL.NamedIndividual)) 
    g.add((User2, RDF.type, Movie_namespace.Rating))
    g.add((User2, Movie_namespace.userId, user_id))
    g.add((User2, Movie_namespace.movieId, movieId))
    g.add((User2, Movie_namespace.rate, rating))

## Ecrire dans un fichier externe 
RDF_file = g.serialize(format='xml')
with open("New_Movie.rdf", 'w', encoding='utf-8') as rdf_output:
        rdf_output.write(RDF_file)


## Modification à faire 

Il y encore quelque petit chose à changer 
1) Il serait peut être plus judicieux de changer l'URI pour ne réutiliser la même que celle de Movie.rdf
2) Dans l'êtat actuel, je ne suis pas sur de respecter les consignes, peut être faudrait-t'il uniquement génerer des individus via un fichier RDF/XML plutôt que de parse l'ontologie de base et d'y ajouter les individus
