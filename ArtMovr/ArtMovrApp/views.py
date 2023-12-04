from django.shortcuts import render
from django.http import request
from SPARQLWrapper import DIGEST, SPARQLWrapper, JSON, BASIC, RDFXML
from rdflib import Graph
from django.views.decorators.csrf import csrf_exempt
from ArtMovrApp.templates import *
from django.shortcuts import render
import stardog
from django.http import HttpResponse

sparql = SPARQLWrapper("https://sd-db794fc3.stardog.cloud:5820/Vfinal/query")
# url = "https://sd-db794fc3.stardog.cloud:5820/<your-database>/query"
# username = "hello"
# password = "hellohello123"

# connection_details = {
#     'endpoint': 'https://sd-db794fc3.stardog.cloud:5820/',
#     'username': 'hello',
#     'password': 'hellohello123'
# }

# def setup_sparql():
#     sparql = SPARQLWrapper("https://sd-db794fc3.stardog.cloud:5820/")
#     sparql.setHTTPAuth(BASIC)
#     sparql.setCredentials("aadmin1", "531project123")
#     return sparql

def setup_sparql():
    sparql = SPARQLWrapper("https://sd-db794fc3.stardog.cloud:5820/Vfinal/query")
    sparql.setHTTPAuth(BASIC)
    sparql.setCredentials('hello', 'hellohello123')
    sparql.setReturnFormat(JSON)
    return sparql

@csrf_exempt 
def search(request):
    search_query = request.GET.get('searchInput', '')
    search_type = request.GET.get('searchType', 'artist')

    if search_type == 'artist':
        return search_artist(search_query)
    elif search_type == 'artwork':
        return search_artwork(search_query)
    else:
        return HttpResponse("Invalid search type", status=400)



def search_artist(artist_name):
    try:
        sparql = setup_sparql()
        # Your SPARQL query setup and execution...
        sparql.setQuery("""
        PREFIX museum: <http://www.semanticweb.org/darsh/ontologies/2023/10/museum#>
        SELECT DISTINCT ?artistName ?nationality ?gender ?constituentID ?bornYear ?deathYear ?artwork ?title
        WHERE {{
            ?artist a museum:Artist ;
                    museum:hasName ?artistName ;
                    museum:hasNationality ?nationality ;
                    museum:hasGender ?gender ;
                    museum:hasConstituentID ?constituentID ;
                    museum:hasBornYear ?bornYear ;
                    museum:hasDeathYear ?deathYear .
            ?artwork museum:hasArtist ?artist ;
                    museum:hasTitle ?title .

            FILTER (regex(?artistName, "{}", "i"))
        }}
        LIMIT 7
    """.format(artist_name))
        results = sparql.query().convert()

        if results:
            # Process results and create context...
            context = {'artists': results}  # Adjust this according to your actual data structure
            return render(request, 'artists.html', context)
        else:
            return render(request, 'artists.html', {'error': 'No results found'})
    except Exception as e:
        print(f"Error in search_artist: {e}")
        return render(request, 'artists.html', {'error': 'Error executing query'})


def search_artwork(artwork_title):
    # SPARQL query for artwork information
    
    sparql.setQuery("""
        YOUR SPARQL QUERY FOR ARTWORK '{}'
        (Adapt this query to match your ontology and data structure)
    """.format(artwork_title))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results:
        artwork_info = extract_artwork_info(results[0])  # Assuming results[0] is the first artwork
        return render(request, 'artworks.html', {'artwork': artwork_info})
    else:
        return render(request, 'artworks.html', {'error': 'No results found'})



def extract_artist_info(result):
    # Extract artist information from result
    # Implement logic based on result structure
    return {
        'name': result.get('Artist'),
        'nationality': result.get('Nationality'),
        'bornYear': result.get('BornYear'),
        'deathYear': result.get('DeathYear'),
        'gender': result.get('Gender'),
        # Add more fields as necessary
    }

def extract_artworks_info(results):
    # Extract artworks information from results
    # Implement logic based on results structure
    artworks = []
    for result in results:
        artworks.append({
            'title': result.get('Title'),
            'date': result.get('Date'),
            'url': result.get('URL'),
            # Add more fields as necessary
        })
    return artworks[:7]  # Limit to 7 artworks

def extract_artwork_info(result):
    # Extract artwork information from result
    # Implement logic based on result structure
    return {
        'title': result.get('Title'),
        'date': result.get('Date'),
        'objectID': result.get('ObjectID'),
        'url': result.get('URL'),
        'department': result.get('Department'),
        'artistName': result.get('Artist'),
        # Add more fields as necessary
    }

def index(request):
    return render(request, 'index.html')