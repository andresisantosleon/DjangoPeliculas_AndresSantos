from django.shortcuts import render
import requests
from VotacionPeliculas.models import Peliculas
from django.db.models import Sum

# Create your views here.

def BusquedaDePeliculas(textoBusqueda, p=''):

    if p=='imdbID':

        url=r'https://www.omdbapi.com/?i=%s&apikey=cba8f360' % textoBusqueda
        
    else:
        url=r'https://www.omdbapi.com/?s=%s&apikey=cba8f360' % textoBusqueda
    
    respuesta=requests.get(url)
    infoPeliculas=respuesta.json()
    peliculasModels=[]

    try:
        infoPeliculas['Error']

    except:  

        try: 
            contenido=infoPeliculas['Search']
            for peli in contenido:
                peliculasModels.append(Peliculas.constructor_1(peli['Title'], peli['imdbID'], 0))
        except:
            contenido=infoPeliculas
            peliculasModels.append(Peliculas.constructor_1(contenido['Title'], contenido['imdbID'], 0))

    return peliculasModels

def PodioPeliculas():
    totalvotos=list(Peliculas.objects.aggregate(Sum('votos')).values())[0]
    primero=Peliculas.objects.order_by('-votos').first() 
    segundo=Peliculas.objects.order_by('-votos').exclude(imdbID=primero.imdbID).first()
    tercero=Peliculas.objects.order_by('-votos').exclude(imdbID__in=[primero.imdbID, segundo.imdbID]).first()
    return [totalvotos, [[primero, '{:.2%}'.format(primero.votos/totalvotos)], [segundo, '{:.2%}'.format(segundo.votos/totalvotos)], [tercero, '{:.2%}'.format(tercero.votos/totalvotos)]]] 

def busquedaPeliculas(request):

    textoEnsayo=''
    peliculasEncontradas=[]

    if request.GET.get('textoBusqueda', '')!='':
        busqueda=request.GET['textoBusqueda']   
        peliculas=BusquedaDePeliculas(busqueda)
    else:
        peliculas=[]

    votos=request.GET.getlist('imdbID',[])
    if votos!=[]:
        for id in votos:
            peliculaVotada=BusquedaDePeliculas(id,'imdbID')[0]

            try:
                peliculaSumaVoto=Peliculas.objects.get(imdbID=peliculaVotada.imdbID)
                peliculaSumaVoto.votos+=1
                peliculaSumaVoto.save()    
            except:
                peliculaVotada.votos=1
                peliculaVotada.save()

            #if Peliculas.objects.get(imdbID=peliculaVotada.imdbID):
                #peliculaVotada.votos+=1
    resulVotaciones=PodioPeliculas()
    return render(request, "busquedaPeliculas.html",{'infoPelis':peliculas, 'podioList':resulVotaciones})