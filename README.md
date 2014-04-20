# Cartelera

Cartelera is the code base that generates the website [CarteleraPerú](http://carteleraperu.com).

CarteleraPerú shows movie times for the three main movie theater chains in Perú (UVK, CinePlanet y Cinemark).  The website generated is static and as lean as posible.  It shows only movie titles, subtitles information, and showtimes.  The information is obtained from the publicly available information published by the theaters. 

Each time the program is run, three static web pages are generated in the directory specified by 'basedir' (see _configuration_):

*  `index.html` is the main page containing movie show times for each theater for each of the main movie theater chains.
*  `preferences.html` is a settings page that allows the user to display or hide theaters from the main page.  Preferences are stored in the user's browser using cookies.
*  `about.html`, the about page.

Jinja2 is used for rendering the pages.  Sample template files can be found in the `templates` directory. 


## Dependencies

The code has been tested in Python 2.7.5 (OSX) and Python 2.7.3 (Linux). It uses BeautifulSoup for obtaining movie information, and Jinja2 for template rendering.

Dependencies can be installed in the current environment using `pip`:

```python
$ pip install -r requirements.txt
```

## Configuration

The directory `settings` contains three files:

* Settings common to production and development environments are specified in `base.py`.  (There should be no need to modify this file.)
* Settings used for development reside in `local.py`. (Intended to be used when running the code on your local machine.)
* Settings used for production reside in `production.py`.

Sample `local.py`.
```python
# website root directory
basedir = "./www"

# jinja2 templates directory
template_dir = './templates'
```

You should at least configure `basedir` and `template_dir`:

*  `basedir` is where the generated website will reside and served by your webserver.
*  `template_dir` is where your template files reside.  For production, it is recommended to specify the full directory path.


## Command line options

The main entry point is `cines.py`.  It accepts only one command line option:  `--dev`.  It runs the program using the settings from `local.py`. 

```python
$ python cines.py --dev
```

If no option is specified, `production.py` settings are assumed.

```python
$ python cines.py
```

## Why

This is a _scratch your own itch_ kind of project.  The movie theater's websites are slow and bloated with irrelevant information.  I wanted a page showed just the movie titles and show times, and loaded as _fast_ as possible.

## TODO

* Unify movie names across movie chains.  The current approach is to use `python-Levenshtein` a movie named different across chains, but it does not always work.

* There is bug that 'sometimes' prevents showing information from Jockey Plaza.

