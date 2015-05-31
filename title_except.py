# coding: utf-8

# Thanks to http://stackoverflow.com/questions/3728655/python-titlecase-a-string-with-exceptions

# No es una lista completa, pero suficiente para cartelera.

exceptions_es = [
	# artículos
	'el', 'la', 'los', 'las', 
	'un', 'una', 'unos', 'unas',
	'lo', 'le', 'les',
	'al', 'del',
	'un', 'unos', 'una', 'unas', 
	# Preposiciones
	'a', 'ante', 'bajo', 'cabe', 'con', 'contra',
	'de', 'desde', 'durante', 'en', 'entre',
	'hacia', 'hasta', 'mediante', 'para',
	'por', u'según', 'segun', 'sin', 'so',
	'sobre', 'tras', 'versus', u'vía', 'via',
	# Adverbios
	u"aquí", u"allí", u"ahí", u"allá", u"acá", u"arriba",
	u"abajo", u"cerca", u"lejos", u"delante", u"detrás",
	u"encima", u"debajo", u"enfrente", u"atrás", u"alrededor",
	u"antes", u"después", u"luego", u"pronto", u"tarde", u"temprano",
	u"todavía", u"aún", u"ya", u"ayer", u"hoy", u"mañana", u"siempre", 
	u"nunca", u"jamás", u"próximamente", u"prontamente", u"anoche", 
	u"enseguida", u"ahora", u"mientras", u"anteriormente",
	u"bien", u"mal", u"regular", u"despacio", u"deprisa", 
	u"así", u"tal", u"como", u"aprisa", u"adrede", u"peor", 
	u"mejor", u"fielmente", u"estupendamente", u"fácilmente", 
	u"negativamente", u"responsablemente",
	u"muy", u"poco", u"mucho", u"bastante", u"más", u"menos",
	u"algo", u"demasiado", u"casi", u"solo", u"solamente",
	u"tan", u"tanto", u"todo", u"nada", u"aproximadamente",
	u"sí", u"también", u"cierto", u"ciertamente", u"efectivamente", u"claro",
	u"exacto", u"obvio", u"verdaderamente", u"seguramente", u"asimismo",
	u"no", u"jamás", u"nunca", u"tampoco",
	u"primeramente", u"últimamente",
	u"quizá", u"quizás", u"acaso", u"probablemente", u"posiblemente", 
	u"seguramente", u"tal vez", u"puede",
	u"cuándo", u"cómo", u"cuánto", u"dónde",
	u"cuando", u"como", u"cuanto", u"donde",
	u"solo", u"solamente", u"aún", u"inclusive", u"además", 
	u"únicamente", u"incluso", u"mismamente", u"propiamente", 
	u"precisamente", u"concretamente", u"viceversa", u"contrariamente", 
	u"siquiera", u"consecuentemente",
	# conjunciones
	u"al", u"por", u"con", u"de", u"para", 
	u"y", u"ni", u"pero", u"sino",
	u"conque", u"luego", u"tan", 
	u"e", u"o", u"u",
	u"que", 
]

import re 
def title_except(s, exceptions=exceptions_es):
	word_list = re.split(' ', s)       #re.split behaves as expected
	final = [word_list[0].capitalize()]
	for word in word_list[1:]:
		final.append(word in exceptions and word or word.capitalize())
	return " ".join(final)


