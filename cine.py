#!/usr/bin/env python
# encoding: utf-8
"""
cine.py

Created by Roberto Zoia on 2012-05-02.
Copyright (c) 2012 8 Consultores SAC. All rights reserved.
"""

#
# Revision history
#
# 2012-05-04
# Changed from urllib2 to urllib3.
# urllib3 opens just an http connection to each site and reuses it.  This results
# in an important speed improvement (dropped total page generation time from 50sec to 30sec) 
#

import urllib3
import re
from bs4 import BeautifulSoup

#
#	Para usar una terminología clara, definimos:
#		Cadena:  UVK, Cinemark Perú, Cineplanet
#		Cines de la cadena:  UVK Larcomar, UVK Caminos del Inca
#		Cartelera:   películas que pasan en uno de los cines
#		Película:  úna película que pasan en un cine
#


class Cine(object):
	"""docstring for Cine"""
		
	def __init__(self, cadena="", tag=""):
		super(Cine, self).__init__()
		
		self.tag = tag
		self.cadena = cadena
		
		# url de la página del cine
		self.url = ""
		
		# encoding usado para la salida de las funciones
		self.encoding = 'utf-8'

		# connection timeout for fetching pages
		self.timeout = 10.0
		
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
			Devuelve la programación del cine en el siguiente formato:
			[ 
				{ 	'pelicula':  'nombre de la película', 
					'horarios':   [ '7:30pm', '8:30pm', '10:30pm'] },
				{ 	'pelicula':  'nombre de la película', 
					'horarios':   [ '7:30pm', '8:30pm', '10:30pm'] },
				(...)
			]
			
			Este método acepta tanto idCines como url como parámetros.  Las clases
			derivadas de Cine deben implementar la funcionalidad respectiva, según 
			la cadena de cines use ids o urls para identificar las páginas de carteleras.
			
		"""
		pass
	
	
	def get_cartelera_cines_de_cadena(self):
		"""
			Devuelve la programación de cada cine de la cadena en el siguiente formato:
			
			[ 
				{ 	'cine': u'UVK Larcomar', 
					'cartelera':  [ la cartelera en el formato de get_programacion_cine ]
				}, 
				{ 	'cine': u'UVK Platino Basadro', 
					'cartelera':  [ la cartelera en el formato de get_programacion_cine ]
				}, 
				(...)
			
			]
		
		
		Returns a list of [ cine,  
									[ [ movie title, [horario, horario, horario, ... ],
									  [ movie title, [horario, horario, horario, ... ],
									],

							]
		"""
		result = []
		for t in self.get_cines_cadena():
			cine, idCine, urlCine = t
			
			if idCine == 0:
				result.append({
					'cine': u"%s" % cine, 
					'cartelera': self.get_programacion_cine(url=urlCine) 
				})
			else:
				result.append({
					'cine': u"%s" % cine, 
					'cartelera': self.get_programacion_cine(idCine=idCine) 
				})
		
		return result
	
	
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
	
	def purify_movie_name(self, s):

		iterList = [ self.suffix_subtitles, self.prefix_subtitles,
			self.suffix_resolutions, self.prefix_resolutions ]


		for listElm in iterList:
			for l in listElm.itervalues():
				for t in l:
					s = s.replace(t, "")
		
		s = s.replace("-", "")
		
		return s.strip()
	
	#
	# Utilities
	#
	def grab_horarios(self, s):
		return self.reHorarios.findall(s)
	
	
	def replace_accents(self, s):
		replacements = [(u'á','a'), (u'é','e'), (u'í', 'i'), (u'ó','o'),(u'ú','u'),
						(u'Á','A'), (u'É', 'E'), (u'Í','I'), (u'Ó','O'), (u'Ú','U'),
			]

		for a, b in replacements:
			s = s.replace(a, b)
		return s
		
	

class CineUVK(Cine):
	"""UVK Multicines"""
	
	def __init__(self):
		super(CineUVK, self).__init__(cadena=u"UVK Multicines",tag="UVK")
		
		self.url = r"""http://www.uvkmulticines.com"""
		self.encoding = 'utf-8'

		# indicadores de subtitulos
		self.suffix_subtitles['doblada'] =  [ u'(Doblada)', u'(Digital doblada)', ]
		self.suffix_subtitles['subtitulada'] = [
				u'(HD Subtitulada)', u'(Subtitulada)', u'(Digital subtitulada)',
			]
				
		# indicadores de resolución
		self.suffix_resolutions['HD'] = [ u'HD', u'(Digital subtitulada)', u'(Digital doblada)', ]
		self.suffix_resolutions['3D'] = [ u'3D', ]
		
		
		# self.suffix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.suffix_resolutions)
		# self.prefix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.prefix_resolutions)
		# self.suffix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.suffix_subtitles)
		# self.prefix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.prefix_subtitles)
		
		
		# conexión reusable al servidor de la cadena
		self.conn = urllib3.connection_from_url(self.url, timeout=self.timeout)
		
		
		
	def get_cines_cadena(self):
				
		# TODO:  sacar esta lista de la página web
		
		result = [
			(u'UVK Platino Basadre', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-PLATiNO-BASADRE-"),
			(u'UVK Larcomar', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-LARCOMAR" ),
			(u'UVK Caminos del Inca',0, r"http://www.uvkmulticines.com/multicines/cine/UVK-CAMiNOS-DEL-iNCA"),
			(u'UVK San Martín Centro', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-SAN-MARTIN-CENTRO"),
			(u'UVK Ica', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-iCA" ),
			(u'UVK Asia', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-ASiA"),
			(u'UVK Huacho', 0,  r"http://www.uvkmulticines.com/multicines/cine/UVK-HUACHO" ),
			(u'UVK El Agustino', 0, r"http://www.uvkmulticines.com/multicines/cine/UVK-EL-AGUSTINO" ),
			
		]
		
		return result
	
	
	def get_programacion_cine(self, idCine=0, url=None):
		
		# UVK usa urls para identificar sus cines, no ids
		# TODO:  handle errors
		
		r = self.conn.request('GET', url)
		
		if r.status == 200:
			# Page readed ok
			
			html = r.data.decode(self.encoding, errors='replace')  
		
			soup = BeautifulSoup(html)
		
			peliculas = soup.find(id = re.compile('highslide-html??')).find_all('td', { 'class': 'bg_infotabla1'})
		
			result = []
		
			for i in range(0, len(peliculas)-1):
				# Identificamos el comienzo del listado de películas porque son los
				# <td> que tienen class bg_infotabla1 y un elemento <a href=...>
			
				if peliculas[i].a is not None:
					# El primer <td> tiene el nombre de la película.
					# El segundo <td> tiene el horario
					result.append({
						'pelicula': self.purify_movie_name(peliculas[i].string), 
						'horarios': self.grab_horarios(peliculas[i+1].string),
						'isSubtitulada': self.is_movie_subtitled(peliculas[i].string),
						'isDoblada': self.is_movie_translated(peliculas[i].string),
						'isHD':  self.is_movie_HD(peliculas[i].string),
						'is3D': self.is_movie_3D(peliculas[i].string)
					})
					i = i +2
				else:
					i = i+1
		
			return result
			
		else:
			return None
	
	

			
	



class CineCMP(Cine):
	"""docstring for CineCMP"""
	
	def __init__(self):
		super(CineCMP, self).__init__(cadena=u"Cinemark", tag="CMP")
		
		self.url = r"""http://www.cinemark-peru.com"""
		
		# indicadores de subtitulos
		self.suffix_subtitles['doblada'] =  [ u'(DOB)', u'(DOB', ]
		self.suffix_subtitles['subtitluada'] = [ u'(SUB)', u'(SUB',]

		# indicadores de resolución
		self.suffix_resolutions['HD'] = [ u'XD', u'XD 3D' ]
		self.suffix_resolutions['3D'] = [ u'3D', ]
		
		# único de Cinemark...
		self.prefix_resolutions['HD'] = [ u'2D Digital', u'2D DIG']
		
		
		# aunque su página diga 'utf-8', el servidor envía iso-8859-15
		# self.encoding = 'iso-8859-15'  
		self.encoding = 'utf-8'
		
		# self.suffix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.suffix_resolutions)
		# self.prefix_resolutions = self.replace_strings_for_regex_in_dict_with_list(self.prefix_resolutions)
		# self.suffix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.suffix_subtitles)
		# self.prefix_subtitles = self.replace_strings_for_regex_in_dict_with_list(self.prefix_subtitles)
		
		self.conn = urllib3.connection_from_url(self.url, timeout=self.timeout)
		
		
	
	def get_cines_cadena(self):
		cines = [
			(u'Jockey Plaza', 740),
			(u'San Miguel', 742),
			(u'Mega Plaza', 743),
			(u'Plaza Lima Sur', 741),
			(u'Aventura Plaza Trujillo', 744),
			(u'Aventura Plaza Bella Vista', 754),
			(u'Open Plaza Angamos', 600),
			(u'Parque Lambramani', 659),
			(u'Open Plaza Piura', 660),
			(u'Aventura Plaza Arequipa', 778),
		]
		
		url = """%s/cine.php?id=%s"""
		result = [ [c, idCine, url % ( self.url, idCine)]  for c, idCine in cines ]
		
		return result
			
	def get_programacion_cine(self, idCine=0, url=None):
		
		url = """%s/cine.php?id=%s""" % (self.url, idCine)
		
		r = self.conn.request('GET', url)
	
		if r.status == 200:
			# En su página dice 'charset=utf-8' pero usan en realidad iso-8859-15
			html = r.data.decode(self.encoding, errors='replace')
		
			soup = BeautifulSoup(html)
		
			# soup tiene ahora la página que contiene la cartelera del cine idCine
			base = soup.find_all('a', { 'id': re.compile('peli-*')})
		
			result = []
		
			for b in base:
				t = b.next_sibling
				while t == '\n':
					t = t.next_sibling
				
				# Get movie title
				tPelicula = t.h2.string.strip()
			
				# Get showtimes for today (first entry on showtime table)
				tHorarios = t.find('tr', { 'class': re.compile('tablelist-values?')}).string.strip()
			
				result.append({
				 	'pelicula': self.purify_movie_name(tPelicula),
				 	'horarios': self.grab_horarios(tHorarios),
					'isSubtitulada': self.is_movie_subtitled(tPelicula),
					'isDoblada': self.is_movie_translated(tPelicula),
					'isHD':  self.is_movie_HD(tPelicula),
					'is3D': self.is_movie_3D(tPelicula)
				})
			
			return result
		else:
			return None


class CineCP(Cine):
	"""Cine implementation for CinePlanet"""
	def __init__(self):
		super(CineCP, self).__init__(cadena=u"Cineplanet", tag="CP")
		
		
		# indicadores de subtitulos
		self.suffix_subtitles['doblada'] =  [ u'Dob', u'3D Dob', ]
		self.suffix_subtitles['subtitluada'] = [
				u'Sub', u'3D Sub', u'HD Sub',
			]

		# indicadores de resolución
		self.suffix_resolutions['HD'] = [ u'Digital', u'Digital Hd', u'HD', u'Hd',  ]
		self.suffix_resolutions['3D'] = [ u'3D', ]
				
		self.url = r"""http://www.cineplanet.com.pe"""
		self.encoding = 'utf-8'
		
		self.cp_server = r"""/cineplanet.server.php"""
		self.conn = urllib3.connection_from_url(self.url, timeout=self.timeout)

	
	def get_cines_cadena(self):
		"""
			Devuelve una lista de los cines y sus urls (o sus ids)
		"""
		result = [
			(u'CinePlanet Alcázar', 4, None),
			(u'CinePlanet Arequipa', 6, None),
			(u'CinePlanet Arequipa Real Plaza', 28,None),
			(u'CinePlanet Centro', 22, None),
			(u'CinePlanet Chiclayo', 13, None),
			(u'CinePlanet Comas', 16, None),
			(u'CinePlanet Huancayo', 20, None),
			(u'CinePlanet Juliaca', 26, None),
			(u'CinePlanet La Molina', 9, None),
			(u'CinePlanet Norte', 7, None),
			(u'CinePlanet Piura', 8, None),
			(u'CinePlanet Primavera', 5, None),
			(u'CinePlanet Risso', 12, None),
			(u'CinePlanet San Miguel', 1, None),
			(u'CinePlanet Santa Clara', 24, None),
			(u'CinePlanet Tacna', 27, None),
			(u'CinePlanet Trujillo Centro', 17, None),
			(u'CinePlanet Trujillo Real Plaza', 19, None),
		]
		return result
	
	
	def get_programacion_cine(self, idCine=0, url=None):

		url = """%s/nuestroscines.php?complejo=%02d""" % (self.url, idCine)

		r = self.conn.request('GET', url)
		
		if r.status == 200:
			html = r.data.decode(self.encoding, errors='replace')\
			
			soup = BeautifulSoup(html)
			peliculas = soup.find_all('a', 
						{ 'href': re.compile('detalle_pelicula.php\?pelicula=.*\&complejo\=%02d' % idCine) } )

			result = [] 

			for i in range(0, len(peliculas)-1, 2):
				tPelicula = peliculas[i].string
				result.append({
				 	'pelicula': self.purify_movie_name(tPelicula), 
					'horarios': self.grab_horarios(peliculas[i+1].contents[0]),
					'isSubtitulada': self.is_movie_subtitled(tPelicula),
					'isDoblada': self.is_movie_translated(tPelicula),
					'isHD':  self.is_movie_HD(tPelicula),
					'is3D': self.is_movie_3D(tPelicula)
					
				})
			
			return result
		else:
			return None


if __name__ == '__main__':
	pass

