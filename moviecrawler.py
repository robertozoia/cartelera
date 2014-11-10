# encoding: utf-8

# moviecrawler.py

# The MIT License (MIT)
#
# Copyright (c) 2012 Roberto Zoia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

#
# Revision history
#
# 2012-05-04
# Changed from urllib2 to urllib3.
# urllib3 opens just an http connection to each site and reuses it.  This results
# in an important speed improvement (dropped total page generation time from 50sec to 30sec) 
#

import os
import urllib3
from urllib3.exceptions import HTTPError, TimeoutError, MaxRetryError
import requests

import re
import datetime

from bs4 import BeautifulSoup

from models import TheaterChain, Theater, Movie
import tools
import title_except

#
#   Para usar una terminología clara, definimos:
#       Cadena:  UVK, Cinemark Perú, Cineplanet
#       Cines de la cadena:  UVK Larcomar, UVK Caminos del Inca
#       Cartelera:   películas que pasan en uno de los cines
#       Película:  úna película que pasan en un cine
#


class MovieCrawler(object):
    """docstring for Cine"""
        
    def __init__(self, cadena="", tag=""):
        
        self.tag = tag
        self.cadena = cadena
        
        # url de la página del cine
        self.url = ""
        
        # encoding usado para la salida de las funciones
        self.encoding = 'utf-8'

        # connection timeout for fetching pages
        self.timeout = 12.0
        
        # regex que catpura los horarios de un string
        self.reHorarios = re.compile(r"""\d{1,2}:\d{2}\s*(?:am|pm|a\.m\.|p\.m\.)*""")
        
        ## prefijos y sufijos que la cadena de cines usa en los títulos de sus películas
        # prefijos que indican subtitulación de la película
        self.prefix_subtitles = {
            'doblada':  [],
            'subtitulada': [],
        }
        
        self.suffix_subtitles = {
            'doblada': [],
            'subtitulada': [],
        } 
        
        # prefijos y sufijos que indican resolúción/calidad de la película
        # las clases derivadas deben modificar esta data para reflejar la cadena de cines específica
        self.prefix_resolutions = {
            'HD': [],
            '3D': [],
        }
        
        self.suffix_resolutions = {
            'HD': [],
            '3D': [],
        }

        self.suffix_dbox = []
        self.suffix_discard = []    

        self.movie_cache = {}

    
        
    def getTheaterChainMovies(self):
        """
            Returns a TheaterChain object with theaters,
            movies and showtimes fetched from the theater theater chain 
            website
        """
        theater_chain = TheaterChain(
            name = self.cadena,
            tag = self.tag,
            theaters = self.get_cartelera_cines_de_cadena()
            )

        return theater_chain


    def get_cines_cadena(self):
        """
        Devuelve una lista que contiene los locales de la cadena de cines en el siguiente
        formato:
        
            [ 
                (u'UVK Larcomar', 0, 
                            r'http://www.uvkmulticines.com/multicines/cine/UVK-LARCOMAR'),
                (u'UVK Platino Basadre', 0,
                            r'http://www.uvkmulticines.com/multicines/cine/UVK-PLATiNO-BASADRE-'),
                (u'[Cine]', [idCine], [url de la página de la cartelera de ese cine])
                (...)
                
            ]
            
            Hay cadenas de cines que usan un id para identificar la página de cartelera de sus cines.
            Otras usan un id para identificar la cartelera de cada cine.
            Si una cadena usa ids, entonces get_cines_cadena devuelve None en vez de un url
            Si una cadena usa urls, entonces get_cines_cadena devuelve idCine = 0
             
        """
        pass
    
    
    def get_programacion_cine(self, idCine=0, url=None):
        """
            Devuelve la programación del cine.
            
            Este método acepta tanto idCines como url como parámetros.  Las clases
            derivadas de Cine deben implementar la funcionalidad respectiva, según 
            la cadena de cines use ids o urls para identificar las páginas de carteleras.
            
        """
        pass
    
    
    def get_cartelera_cines_de_cadena(self):
        """
            Returns a list of Theater objects.
        """
        result = []

        for t in self.get_cines_cadena():
            cine, idCine, urlCine = t
            
            theater = Theater(name=cine)

            if idCine == 0:
                theater.movies  = self.get_programacion_cine(url=urlCine)
            else:
                theater.movies = self.get_programacion_cine(idCine=idCine)
                
            # print "Theaters for %s: %s" % (self.tag, theater)

            result.append(theater)

        return result
    
    
    #
    # Utility methods
    # 

    def is_movie_translated(self, s):
        result = False
        
        for r in self.suffix_subtitles['doblada']:
            if s.find(r) != -1:
                result = True
                break
        
        if not result:
            for r in self.prefix_subtitles['doblada']:
                if s.find(r) != -1:
                    result = True
                    break
            
        return result
                
    
    def is_movie_subtitled(self, s):
        """
            Returns true if movie is subtitled.
            Uses theater-specific prefixes and 
        """
        
        result = False
            
        for r in self.suffix_subtitles['subtitulada']:
            if s.find(r) != -1:
                result = True
                break
        
        # Un temita es que en varios casos, si la película no dice nada,
        # por defecto es subtitulada.  
                
        if not result:
            result = not self.is_movie_translated(s)
            
        return result
        
        
    def is_movie_HD(self, s):
        
        result = False
        for r in self.suffix_resolutions['HD']:
            if s.find(r) != -1:
                result = True
                break
            
        if not result:
            for r in self.prefix_resolutions['HD']:
                if s.find(r) != -1:
                    result = True
                    break
        
        return result
        
        
    def is_movie_3D(self, s):
        
        result = False
        for r in self.suffix_resolutions['3D']:
            if s.find(r) != -1:
                result = True
                break
            
        if not result:
            for r in self.prefix_resolutions['3D']:
                if s.find(r) != -1:
                    result = True
                    break
        
        return result

    def is_movie_dbox(self, s):

        result = False
        if self.suffix_dbox:

            for r in self.suffix_dbox:
                if s.find(r) != -1:
                    result = True
                    break

        return result

    
    def purify_movie_name(self, s):

        iterList = [ 
            self.suffix_resolutions, self.prefix_resolutions,
            self.suffix_subtitles, self.prefix_subtitles,   
        ]

        
        for listElm in iterList:
            for l in listElm.itervalues():
                for t in l:
                    s = s.replace("-", "")
                    s = " ".join(s.split()) # purge multiple spaces
                    s = s.replace(t, "")
                    
        
        for t in self.suffix_discard:
            s = s.replace(t, "")
        
        if self.suffix_dbox:
            for r in self.suffix_dbox:
                s = s.replace(r, "")

        s = title_except.title_except(s.lower())
            
        return s.strip()

    def sort_movies(self, movies):
        """
        Sorts movie dict by movie name.
        """
        
    

    def convert_showtime_to_timeobject(self, showtime):
        """
            Takes a showtime as string and returns a 24H formated time.
            Handle quirks in movie chains showtimes.
        """
        suffixes = [('pm', 12), ('p.m.', 12), ('am',0), ('a.m.',0)]
        
        offset = 12  #  by default, all showtimes are pm, even if not stated

        for sfx, off in suffixes:
            if sfx in showtime:
                showtime = showtime.replace(sfx, '')
                offset = off

        # split hours, minutes
        hours, minutes = showtime.split(':')
        hours = int(hours)
        minutes = int(minutes)

        if (hours == 12) and (offset == 12):  offset = 0

        try:
            result = datetime.time(int(hours)+offset, int(minutes)).strftime('%H:%M')
        except ValueError:
            result = datetime.time(int(hours), int(minutes)).strftime('%H:%M')

        return result

    def grab_horarios(self, s):

        return [ self.convert_showtime_to_timeobject(t) for t in self.reHorarios.findall(s)]


    def replace_accents(self, s):
        replacements = [(u'á','a'), (u'é','e'), (u'í', 'i'), (u'ó','o'),(u'ú','u'),
                        (u'Á','A'), (u'É', 'E'), (u'Í','I'), (u'Ó','O'), (u'Ú','U'),
            ]

        for a, b in replacements:
            s = s.replace(a, b)
        return s



#
# Cinépolis
# 


class MovieCrawlerCinepolis(MovieCrawler):

    def __init__(self):
        super(MovieCrawlerCinepolis, self).__init__(cadena=u"Cinépolis", tag="CPOL")

        self.url = r"""http://www.cinepolis.com.pe"""
        self.encoding = 'utf-8'

        self.suffix_subtitles['doblada'] = [
            u'Dob',
        ]

        self.suffix_subtitles['subtitulada'] = [

        ]

        self.suffix_resolutions['HD'] = [
            u'Dig',
        ]


        self.conn = urllib3.connection_from_url(self.url, timeout = self.timeout)



    def get_cines_cadena(self):

        pass


    def get_programacion_cine(self):

        pass


    def get_cartelera_cines_de_cadena(self):
        """
            Returns a list of Theater objects.
        """

        def get_movies(url):

            retries = 3
            result = []
            while retries > 0:
                try:    
                    r = self.conn.request(
                        'GET', 
                        url,
                        headers = urllib3.make_headers(user_agent=wanderer())
                    )
                    break
                except TimeoutError:
                    retries = retries - 1  


            if retries > 0:
                if r.status == 200:
                    # Page readed ok
                    html = r.data.decode(self.encoding, errors='replace')            
                    soup = BeautifulSoup(html)

                    theater_names = [t.string for t in soup.find_all(
                        'span', class_='TitulosBlanco'
                    )]

                    theater_codes = [ t['id'][4:] for t in soup.find_all(
                        'a', id=re.compile('^Cine*')
                    )]


                    
                    for i in range(0, len(theater_names)):

                        theater = Theater(name=theater_names[i])
                        movies = []

                        tmp = soup.find_all('a', id=re.compile(
                            '^idPelCine.+' + theater_codes[i]
                        ))
                        
                        for p in tmp:
                            movie_name = p.parent.find('a', class_='peliculaCartelera').string
                            movie_showtimes = [t.string for t in p.parent.parent.find_all(
                                'span', class_=re.compile('^horariosCartelera*')
                            )]

                            movie_showtimes = self.grab_horarios(" ".join(movie_showtimes))


                            movie = Movie(
                                name = self.purify_movie_name(movie_name),
                                showtimes = movie_showtimes,
                                isSubtitled = self.is_movie_subtitled(movie_name),
                                isTranslated = self.is_movie_translated(movie_name),
                                isHD = self.is_movie_HD(movie_name),
                                is3D = self.is_movie_3D(movie_name),
                                isDbox = self.is_movie_dbox(movie_name),
                            )

                            movies.append(movie)
                            # movies.sort(key=lambda x: x.name)

                        theater.movies = movies

                        result.append(theater)
                else:
                    return []
            else:
                return []

            return result

        
        urls = [
            r"http://www.cinepolis.com.pe/_CARTELERA/cartelera.aspx?ic=100",
            r"http://www.cinepolis.com.pe/_CARTELERA/cartelera.aspx?ic=143",
        ]
        theaters = []

        for u in urls:
            theaters = theaters + get_movies(u)

        return theaters

#
#  UVK
#
class MovieCrawlerUVK(MovieCrawler):
    """UVK Multicines"""
    
    def __init__(self):
        super(MovieCrawlerUVK, self).__init__(cadena=u"UVK Multicines",tag="UVK")
        
        self.url = r"""http://www.uvkmulticines.com"""
        self.encoding = 'utf-8'

        # indicadores de subtitulos
        # (indicador también del desorden cerebral de los encargados del website de UVK)
        self.suffix_subtitles['doblada'] =  [ 
                u'(Estreno Doblada)', u'(HD Doblada)', u'(Digital doblada)', u'(Doblada)',
                u'( Doblada)',
            ]
        self.suffix_subtitles['subtitulada'] = [
                u'(Estreno Subtitulada)', u'(HD Subtitulada)', u'(Digital subtitulada)', 
                u'(Subtitulada)', u'( Subtitulada)',
            ]
                
        # indicadores de resolución
        self.suffix_resolutions['HD'] = [ u'(HD Doblada)', u'(Digital subtitulada)', u'(Digital doblada)', u'HD']
        self.suffix_resolutions['3D'] = [ u'3D', ]
        
        self.suffix_discard = [ '(Estreno)', ]
        
        self.conn = urllib3.connection_from_url(self.url, timeout=self.timeout)
        
        
        
    def get_cines_cadena(self):
                
        # TODO:  sacar esta lista de la página web
        
        result = [
            (u'Platino Basadre', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-PLATiNO-BASADRE-"),
            (u'Larcomar', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-LARCOMAR" ),
            (u'Caminos del Inca',0, r"http://www.uvkmulticines.com/multicines/cine/UVK-CAMiNOS-DEL-iNCA"),
            (u'San Martín Centro', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-SAN-MARTIN-CENTRO"),
            (u'Ica', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-iCA" ),
            (u'Asia', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-ASiA"),
            (u'Huacho', 0,  r"http://www.uvkmulticines.com/multicines/cine/UVK-HUACHO" ),
            (u'El Agustino', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-EL-AGUSTINO" ),
            (u'Piura', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-PiURA"),
            
        ]
        
        return result
    
    
    def get_programacion_cine(self, idCine=0, url=None):
        
        # UVK usa urls para identificar sus cines, no ids
        # TODO:  handle errors

        retries = 3

        while retries > 0:
            try:    
                r = self.conn.request(
                    'GET', 
                    url,
                    headers = urllib3.make_headers(user_agent=wanderer())
                )
                break
            except TimeoutError:
                retries = retries - 1  

        if retries > 0:
            if r.status == 200:
                # Page readed ok
                html = r.data.decode(self.encoding, errors='replace')  
                # html = r.text.encode(r.encoding, errors='replace')            
                soup = BeautifulSoup(html, 'html5lib')
            
                p1 = soup.find('div', class_='highslide-body')
                
                if p1:
                    peliculas = p1.find_all('td', class_='bg_infotabla1')
                else:
                    return []

            
                result = []
            
                for i in range(0, len(peliculas)-1):
                    # Identificamos el comienzo del listado de películas porque son los
                    # <td> que tienen class bg_infotabla1 y un elemento <a href=...>
                
                    if peliculas[i].a is not None:
                        # El primer <td> tiene el nombre de la película.
                        # El segundo <td> tiene el horario

                        movie = Movie(
                            name = self.purify_movie_name(peliculas[i].string),
                            showtimes = self.grab_horarios(peliculas[i+1].string),
                            isSubtitled = self.is_movie_subtitled(peliculas[i].string),
                            isTranslated = self.is_movie_translated(peliculas[i].string),
                            isHD = self.is_movie_HD(peliculas[i].string),
                            is3D =self.is_movie_3D(peliculas[i].string),
                            isDbox = self.is_movie_dbox(peliculas[i].string),
                        )

                        result.append(movie)
                        i = i +2
                    else:
                        i = i+1
            
                # Sort movies
                result.sort(key=lambda x: x.name)
                
                return result
                
            else:
                return []
        else:
            return []


class MovieCrawlerCMP(MovieCrawler):
    """docstring for CineCMP"""
    
    def __init__(self):
        super(MovieCrawlerCMP, self).__init__(cadena=u"Cinemark", tag="CMP")
        
        self.url = r"""http://www.cinemark-peru.com"""
        
        # indicadores de subtitulos
        self.suffix_subtitles['doblada'] =  [ u'(DOB)', u'(DOB', ]
        self.suffix_subtitles['subtitluada'] = [ u'(SUB)', u'(SUB',]

        # indicadores de resolución
        self.suffix_resolutions['HD'] = [ u'XD', u'XD 3D' ]
        self.suffix_resolutions['3D'] = [ u'3D', ]
        
        # único de Cinemark...
        self.prefix_resolutions['HD'] = [ u'2D Digital', u'2D DIG']
        
        self.suffix_discard = [ '2D', ]

        self.suffix_dbox = [ 'd-box', 'D-Box', 'D-box', 'D-BOX', 'DBOX', 'dbox', 'Dbox',  ]
        
        # aunque su página diga 'utf-8', el servidor envía iso-8859-15
        # self.encoding = 'iso-8859-15'  
        self.encoding = 'utf-8'
        
        # self.suffix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.suffix_resolutions)
        # self.prefix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.prefix_resolutions)
        # self.suffix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.suffix_subtitles)
        # self.prefix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.prefix_subtitles)
        
        self.conn = urllib3.connection_from_url(self.url, timeout=self.timeout)
        
        
    
    def get_cines_cadena(self):

#        cines = [
#             (u'Jockey Plaza', 740),
#             (u'San Miguel', 742),
#             (u'Mega Plaza', 743),
#             (u'Plaza Lima Sur', 741),
#             (u'Aventura Plaza Trujillo', 744),
#             (u'Aventura Plaza Bella Vista', 754),
#             (u'Open Plaza Angamos', 600),
#             (u'Parque Lambramani', 659),
#             (u'Open Plaza Piura', 660),
#             (u'Aventura Plaza Arequipa', 778),
#         ]

        cines = [
            (u'Jockey Plaza', '/cines/jockey-plaza'),
            (u'San Miguel', '/cines/san-miguel'),
            (u'Mega Plaza', '/cines/mega-plaza'),
            (u'Plaza Lima Sur', '/cines/plaza-lima-sur'),
            (u'Aventura Plaza Trujillo', '/cines/mall-aventura-plaza-trujillo'),
            (u'Aventura Plaza Bella Vista', '/cines/mall-aventura-plaza-bellavista'),
            (u'Open Plaza Angamos', '/cines/open-plaza-angamos'),
            (u'Parque Lambramani', '/cines/parque-lambramani'),
            (u'Open Plaza Piura', '/cines/open-plaza-piura'),
            (u'Aventura Plaza Arequipa', '/cines/mall-aventura-plaza-arequipa'),
        ]
        
        url = """%s%s"""
        result = [ [c, 0, url % ( self.url, u)]  for c, u in cines ]
        
        return result
            
    def get_programacion_cine(self, idCine=0, url=None):
    
    
        def only_today(l):
    
            months = [ 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic']
            
            # build string for today in CMP format (i.e., '07 Feb')
            dt = datetime.datetime.utcnow()
            today_tag = "%02d %s" % (dt.day, months[dt.month-1].upper())
    
            result = []
            for elm in l:
                if elm.text.upper() == today_tag:
                    result.append(elm)
            return result
            
        

        retries = 3

        while retries > 0:
            try:
                r = self.conn.request('GET', url)
                break
            except TimeoutError:
                retries = retries - 1

        if retries > 0:
            if r.status == 200:
                # En su página dice 'charset=utf-8' pero usan en realidad iso-8859-15
                html = r.data.decode(self.encoding, errors='replace')
            
                soup = BeautifulSoup(html)            
                base = soup.find_all('h4')
                
                # keep only today movies and showtimes
                base = only_today(base)
                
                result = []

                for elm in base:
                    z = elm.next_sibling.next_sibling
                    tmpPeliculas = z.find_all('h5')
                    tmpHorarios = z.find_all('ul')
                    tmp_list = zip(tmpPeliculas, tmpHorarios)
                    
                    for p, h in tmp_list:
                        tPelicula = p.text.strip()
                        tHorarios = h.text.strip()
                                                
                        movie = Movie(
                            name = self.purify_movie_name(tPelicula),
                            showtimes = self.grab_horarios(tHorarios),
                            isSubtitled = self.is_movie_subtitled(tPelicula),
                            isTranslated = self.is_movie_translated(tPelicula),
                            isHD = self.is_movie_HD(tPelicula),
                            is3D = self.is_movie_3D(tPelicula),
                            isDbox = self.is_movie_dbox(tPelicula),
                        )
            
                        result.append(movie)
                
                # Sort movies
                result.sort(key=lambda x: x.name)
                return result
                
            else:
                return []
        else:
            return []

def wanderer():
    return "The Crawler"
    

class MovieCrawlerCP(MovieCrawler):
    """Cine implementation for CinePlanet"""
    def __init__(self):
        super(MovieCrawlerCP, self).__init__(cadena=u"Cineplanet", tag="CP")
        

        
        # indicadores de subtitulos
        self.suffix_subtitles['doblada'] =  [ 
            u'2D Doblada', 
            u'3D Doblada', 
            u'Doblada',
        ]

        self.suffix_subtitles['subtitluada'] = [
                u'Subtitulada', u'2D Subtitulada',
                u'3D Subtitulada',
            ]

        # indicadores de resolución
        self.suffix_resolutions['HD'] = [ u'Digital', u'Digital Hd', u'HD', u'Hd',  ]
        self.suffix_resolutions['3D'] = [ u'3D', ]
        
        self.suffix_discard = [  ]
        
                
        self.url = r"""https://cineplanet.com.pe"""
        self.encoding = 'utf-8'
        
        
        urllib3.make_headers(user_agent=wanderer())
        
        self.conn = urllib3.connectionpool.connection_from_url(
            self.url, 
            timeout=self.timeout,
            headers=wanderer()
        )
        
    
    def get_cines_cadena(self):
        """
            Devuelve una lista de los cines y sus urls.
            Este método fue modificado el 2014-09-26 porque Cineplanet cambió
            su página web (cambió para mejor:  más ordenada y gráficamente más
            amigable).
        """

        result = []

        tipo_salas = [ 'cines-lima', 'cines-provincias']

        for sala in tipo_salas:
    
            retries = 5
            while retries > 0:
                try:
                    r = self.conn.request(
                        'GET', 
                        os.path.join(self.url, sala),
                        headers ={ 'user-agent': wanderer() }
                    )
                    break
                except TimeoutError:
                    retries = retries - 1

            if retries > 0:

                if r.status == 200:
                    html = r.data.decode(self.encoding, errors='replace')
                    soup = BeautifulSoup(html)

                    # Get all cines for this kind of sala
                    t_cines = soup.find_all('div', { 'class': 'WEB_cineListadoNombre' })
                    
                    for c in t_cines:
                        tmp = []
                        tmp.append(c.a.text)
                        tmp.append(0)
                        tmp.append(os.path.join(self.url, c.a['href']))
                        result.append(tmp)


        # Salas prime
        # Cineplanet uses Javascript to generate the data for its prime theaters.
        # So we choose the easiest way (perhaps not the best...): hardcode the urls.

 
        result.append([u'Salaverry', 0, os.path.join('/cine/salaverry')])
        result.append([u'San Borja (La Rambla)', 0, os.path.join('/cine/san-borja')])
        result.append([u'Plaza San Miguel', 0, os.path.join('/cine/san-miguel')])

        return result

    
    def get_programacion_cine(self, idCine=0, url=None):

        

        retries = 5

        while retries > 0:
            try:
                r = self.conn.request(
                        'GET', 
                        url,
                        headers ={ 'user-agent': wanderer() }
                )
                
                break
            except TimeoutError:
                retries = retries -1

        if retries > 0:
        
            if r.status == 200:
                html = r.data.decode(self.encoding, errors='replace')
                soup = BeautifulSoup(html)


                movies = soup.find_all('div', {'class': 'WEB_cineCarteleraDetalle'} )
                result = [] 

                for movie in movies:

                    tipo = movie.find('p', { 'class': 'WEB_peliculaTipo'} ).text.strip()
                
                    t_movie = Movie(

                        name = self.purify_movie_name(
                            movie.find('p', { 'class': 'WEB_cinePeliculaNombre' }).text.strip()
                        ),

                        showtimes = self.grab_horarios(
                            " ".join(
                                [ t.text for t in movie.find_all(
                                    'a', { 'class': 'horarioDisponible' }
                                )]
                            )
                        ),

                        isSubtitled = self.is_movie_subtitled(tipo),
                        isTranslated = self.is_movie_translated(tipo),
                        isHD = self.is_movie_HD(tipo),
                        is3D = self.is_movie_3D(tipo),
                        isDbox = self.is_movie_dbox(tipo),
                    )

                    result.append(t_movie)


                # Sort movies
                result.sort(key=lambda x: x.name)
                return result
                
            else:
                return []
        else:
            return []




