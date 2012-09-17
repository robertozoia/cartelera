#/usr/bin/env python
# encoding: utf-8

# models.py

"""
	Models for cine management
"""


class TheaterChain(object):

	def __init__(self, name=None, tag=None, theaters=[]):
		self.name = name
		self.tag = tag
		self.theaters = theaters

	def __unicode__(self):
		return self.name


class Theater(object):
	
	def __init__(self, name=None, movies=[]):
	
		"""
			Parameters:
			name:			name of this theater
			theater_chain:	a TheaterChain object indicating the chain this
				theater belongs to.

		"""	

		self.name = name
	
		self.movies = movies	# a list of Movie objects


	def __unicode__(self):
		return self.name



class Movie(object):
	"""
		Esta clase contiene toda la información de la película
	"""


	def __init__(self, name=None, showtimes = [],
			isSubtitled=True, isTranslated=True, isHD=False, is3D=False ):

		self.name = name

		self.showtimes = showtimes	# a list of showtimes (as strings)
		self.isSubtitled = isSubtitled
		self.isTranslated = isTranslated
		self.isHD = isHD
		self.is3D = is3D

		self.imdb_canonical_title  = ""
		self.imdb_rating = 0

	def __unicode__(self):
		return self.name



if __name__ == '__main__':
	pass


