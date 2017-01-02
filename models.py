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

import json


class TheaterChain(object):

	def __init__(self, name=None, tag=None, theaters=[]):
		self.name = name
		self.tag = tag
		self.theaters = theaters

	def __unicode__(self):
		return self.name

	def json_dumps(self):
		
		r['name'] = self.name
		r['tag'] = self.tag

		tmp = []

		for th in self.theaters:
			tmp.append(th.json_dumps())

		r['theaters'] = ", ".join(tmp)


	def json_loads(self, d):

		tmp = json.loads(d)

		self.name = tmp['name']
		self.tag = tmp['tag']

		th = []
		for t in tmp['theaters']:
			tTh = Theater()
			tTh.json_loads(t)
			th.append(tTh)

		self.theaters = th
		


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

	def json_dumps(self):
		
		m = []
		for m in self.movies:
			m.append(m.json_dumps())

		r = json.dumps(self.name)
		r['movies'] = ", ".join(m)

		return r		

	def json_loads(self, d):

		movies = []
		tmp = json.loads(d)

		self.name = tmp['name']

		for m in tmp['movies']:
			tM = Movie()
			tM.json_loads(m)
			movies.append(tM)

		self.movies = movies

		



class Movie(object):
	"""
		Esta clase contiene toda la información de la película
	"""


	def __init__(self, name=None, showtimes = [],
			isSubtitled=True, isTranslated=True, isHD=False, is3D=False, isDbox=False):

		self.name = name

		self.showtimes = showtimes	# a list of showtimes (as strings)
		self.isSubtitled = isSubtitled
		self.isTranslated = isTranslated
		self.isHD = isHD
		self.is3D = is3D
		self.isDbox = isDbox

		
	def __unicode__(self):
		return self.name

	def json_dumps(self):
		return json.dumps(self.__dict__)

	def json_loads(self, d):

		tmp = json.loads(d)
		
		self.name = tmp['name']
		self.showtimes = tmp['showtimes']
		self.isSubtitled = tmp['isSubtitled']
		self.isTranslated = tmp['isTranslated']
		self.isHD = tmp['isHD']
		self.is3D = tmp['is3D']
		self.isDbox = tmp['isDbox']






