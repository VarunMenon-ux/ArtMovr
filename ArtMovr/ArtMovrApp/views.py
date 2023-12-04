from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, RDFXML
from SPARQLWrapper.Wrapper import JSON
from rdflib import Graph
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def searchArtwork(keystring):
    #artworkURL=[]
    artworkTitle=[]
    #artistId=[]
    #artistName=list()
    #artistPublicCaption=list()
    #artistImage=list()
    sparql = SPARQLWrapper("https://sd-db794fc3.stardog.cloud:5820")

    sparql.setQuery("""
    SELECT DISTINCT ?obj_2 ?obj_1 ?obj_0
    FROM <tag:stardog:api:context:default>
    FROM <tag:stardog:designer:Vfinal:data:MetObjects>
    FROM <tag:stardog:designer:Vfinal:data:Artworks>
    WHERE {
    {
        ?obj_0 a http://www.semanticweb.org/darsh/ontologies/2023/10/museum#Artist .
        ?obj_1 a http://www.semanticweb.org/darsh/ontologies/2023/10/museum#Artwork .
        ?obj_2 a http://www.semanticweb.org/darsh/ontologies/2023/10/museum#Department .
        ?obj_0 http://www.semanticweb.org/darsh/ontologies/2023/10/museum#hasCreated ?obj_1 .
        ?obj_1 http://www.semanticweb.org/darsh/ontologies/2023/10/museum#hasDepartment ?obj_2 .

  }
}
    }
    Limit 5
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    results=result['results']['bindings']


    for i in results:
        try:
            #artworkImage.append(i['artworkImage']['value'])
            artworkTitle.append(i['title']['value'])
            #artworkWidth.append(i['width']['value'])
            #artistId.append(i['artistID']['value'])
        except:
            pass
'''
    #print(artistId)
    #for i in artistId:
        #sparql.setQuery( """
        #PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        #PREFIX owl: <http://www.w3.org/2002/07/owl#>
        #PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        #PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        #PREFIX ds: <http://purl.org/ctic/dcat#>
        #PREFIX art: <http://w3id.org/art/terms/1.0/>
        #PREFIX awssource1: <http://ec2-18-237-20-56.us-west-2.compute.amazonaws.com:3030/location-data/>
        #PREFIX awssource2: <http://ec2-35-89-102-140.us-west-2.compute.amazonaws.com:3030/artwork-data/>
        #PREFIX awssource3: <http://ec2-18-237-11-218.us-west-2.compute.amazonaws.com:3030/artist-data/>
        #PREFIX artist:<http://www.semanticweb.org/rahul/ontologies/2021/10/sam-artist#>
        #PREFIX artwork:<http://www.semanticweb.org/rahul/ontologies/2021/10/SAAM_Artwork#>
        #PREFIX location:<http://www.semanticweb.org/rahul/ontologies/2021/10/location#>

        SELECT DISTINCT ?FirstName ?LastName ?publicCaption ?artistImage
        WHERE {
        SERVICE awssource3:sparql {
        ?artist artist:hasName ?FirstName.
        ?artist artist:hasLastName ?LastName.
        ?artist artist:hasImageURL ?artistImage.
        ?artist artist:hasPubliccation ?publicCaption.
        ?artist artist:hasArtistID ?ArtistID2.
        FILTER (?ArtistID2 =""" + '"'+ i +'"'+ """)
        }
        }
        """)


        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        print(result)

        results=result['results']['bindings']

        try:
            artistFirstName.append(results[0]['FirstName']['value'])
        except:
            artistFirstName.append("Unavailable")
        try:
            artistLastName.append(results[0]['LastName']['value'])
        except:
            artistLastName.append("Unavailable")
        try:
            artistPublicCaption.append(results[0]['publicCaption']['value'])
        except:
            artistPublicCaption.append("Unavailable")
        try:
            artistImage.append(results[0]['artistImage']['value'])
        except:
            artistImage.append("Unavailable")

   '''
    #return artworkImage, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage
    return artworkTitle
    

@csrf_exempt 
def searchByName(request):
    keyString=""
    if(request.method=='POST'):
        keyString=request.POST['fname']
    
    artworkImages, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage =searchArtwork(keyString)
    return render(request, 'searchByArtwork.html', {'artworkImages':artworkImages,'artworkWidth':artworkWidth,'artworkTitle':artworkTitle,'artistFirstName':artistFirstName,'artistLastName':artistLastName,'artworkTitle':artworkTitle,'artistImage':artistImage, 'artistPublicCaption':artistPublicCaption,'keystring':keyString})

