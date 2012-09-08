#!/usr/bin/env python
# encoding: utf-8
"""
test_cine.py

Created by Roberto Zoia on 2012-06-22.
Copyright (c) 2012 8Consultores SAC All rights reserved.
"""


import unittest
import re

import cine


class test_cine(unittest.TestCase):
	
	data_subtituladas = { 
		"UVK" : [ 
			# UVK
			("El Conspirador", True),   # UVK:  si no dice otra cosa, es subtitulada
			("Prometeo 3D (Subtitulada)", True),
			("Madagascar 3 (Doblada)", False), 
			("Batman: El Caballero de la Noche Asciende (Digital subtitulada)", True), 
		],
		"CMP" : [
			# Cinemark
			("2D DIG BLANCA NIEVES Y EL CAZADOR (SUB)", True),
			("MADAGASCAR 3 (DOB)", False),
			("LA ERA DEL HIELO 4", True),    # Cinemark:  si no dice otra cosa, es subtitulada
		],
		"CP" : [
			# Cineplanet
			("Blancanieves Y El Cazador Dob", False),
			("Sombras Tenebrosas Sub", True), 
		],	
	}
	
	data_dobladas = {
		"UVK"  : [( "Madagascar 3 3D (Doblada)", True), ("La Era de Hielo 4", False), 
			("La Era de Hielo 4 (Digital doblada)", True), 
		],
		"CMP"  : [("MADAGASCAR 3 (DOB)", True), ("HOMBRES DE NEGRO 3 (SUB)", False), 
			("EL PLAN PERFECTO", False)
			],
		"CP"   : [("Madagascar 3 - 3D Dob", True), ("Prometeo 3D Sub", False)],
	}
	
	data_HD = {
		"UVK": [("Tenemos que Hablar de Kevin HD", True), 
				("Batman: El Caballero de la Noche Asciende (Digital subtitulada)", True),
		],
		"CMP": [("XD 3D LA ERA DEL HIELO 4 (DOB)", True), ("2D DIG BLANCA NIEVES Y EL CAZADOR (SUB)", True), 
			("PROMETEO", False)
		],
		"CP": [("Concierto Rolling Stones Hd", True), ("Los Vengadores Dob", False)
		]
	}
	
	data_3D = { 
		"UVK": [("La Era de Hielo 4 3D", True), ("Madagascar 3 3D (Doblada)", True),
		 	("Blanca Nieves y el Cazador", False)
		],
		"CMP": [("3D HOMBRES DE NEGRO 3 (SUB)", True), ("XD 3D LA ERA DEL HIELO 4 ", True),
		 	("2D DIG BLANCA NIEVES Y EL CAZADOR (SUB)", False), ("EL CONSPIRADOR", False)
		],
		"CP": [("Madagascar 3 - 3D Dob", True), ("Prometeo 3D Sub", True), 
			("Sombras Tenebrosas Sub", False)
		],
	}
	
	data_strip = {
		"UVK": [
			("La Era de Hielo 4 3D", "La Era de Hielo 4"), 
			("Madagascar 3 3D (Doblada)", "Madagascar 3"),
			("Blanca Nieves y el Cazador", "Blanca Nieves y el Cazador"),
			("Batman: El Caballero de la Noche Asciende (Digital subtitulada)", 
					"Batman: El Caballero de la Noche Asciende"),
		],
		"CMP": [
			("3D HOMBRES DE NEGRO 3 (SUB)", "Hombres de Negro 3"),
			("XD 3D LA ERA DEL HIELO 4 ", "La Era del Hielo 4"),
			("2D DIG BLANCA NIEVES Y EL CAZADOR (SUB)", "Blanca Nieves y el Cazador"),
			("EL CONSPIRADOR", "El Conspirador")
		],
		"CP": [
			("Madagascar 3 - 3D Dob", "Madagascar 3"),
			("Prometeo 3D Sub", "Prometeo"), 
			("Sombras Tenebrosas Sub", "Sombras Tenebrosas")
		],
	}
	
	def setUp(self):
		self.tags = ["UVK", "CMP", "CP"]
		
		self.cadenas = { 
			"UVK": cine.CineUVK(),
		 	"CMP": cine.CineCMP(), 
			"CP": cine.CineCP()
		}
		
	
	
	def test_is_movie_translated(self):
		
		for tag in self.tags:
			if len(self.data_dobladas[tag]) > 0:
				for t in self.data_dobladas[tag]:
					t_movie, t_dob = t
					result = self.cadenas[tag].is_movie_translated(t_movie)
					self.assertEqual(result, t_dob)
				
	
	
	def test_is_movie_subtitled(self):
		
		for tag in self.tags:
			if len(self.data_subtituladas[tag]) > 0:
				for t in self.data_subtituladas[tag]:
					t_movie, t_sub = t
					result = self.cadenas[tag].is_movie_subtitled(t_movie)
					self.assertEqual(result, t_sub)
	
	
	def test_is_movie_HD(self):
		
		for tag in self.tags:
			if len(self.data_HD[tag]) > 0:
				for t in self.data_HD[tag]:
					t_movie, t_hd = t
					result = self.cadenas[tag].is_movie_HD(t_movie)
					self.assertEqual(result, t_hd)
	
	
	def test_is_movie_3D(self):
		for tag in self.tags:
			if len(self.data_HD[tag]) > 0:
				for t in self.data_3D[tag]:
					t_movie, t_3d = t
					result = self.cadenas[tag].is_movie_3D(t_movie)
					self.assertEqual(result, t_3d)
	
	
	def test_purify_movie_name(self):
		
		for tag, list in self.data_strip.items():
			for t_value, t_result in list:
				result = self.cadenas[tag].purify_movie_name(t_value)
				self.assertEqual(result.lower(), t_result.lower())
			
	


if __name__ == '__main__':
	unittest.main()