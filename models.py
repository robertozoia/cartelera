# encoding: utf-8

# models.py

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

		
	def __unicode__(self):
		return self.name



