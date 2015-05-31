# Makefile for cartelera
# This makefile concatenates and minifies .js and .css files for production
# Requires yuicompressor

YUICOMPRESSOR = java -jar ~/bin/yuicompressor.jar

# CSS files.  Order is important here
CINES_CSS_FILES = css/bootstrap.min.css css/bootstrap-theme.css css/addtohomescreen.css css/cines.css 
CINES_CSS_ALL = css/cines-all.css
CINES_CSS_ALL_MIN = css/cines-all.min.css

CINES_JS_FILES = js/jquery-1.11.1.min.js js/json2.js js/jquery.cookie.js js/bootstrap.min.js \
			js/addtohomescreen.min.js js/cines.js
CINES_JS_ALL = js/cines-all.js
CINES_JS_ALL_MIN = js/cines-all.min.js

PREFERENCES_CSS_FILES = css/bootstrap.min.css css/bootstrap-theme.css \
					   css/switchery.min.css css/cines.css
PREFERENCES_CSS_ALL = css/preferences-all.css
PREFERENCES_CSS_ALL_MIN = css/preferences-all.min.css

PREFERENCES_JS_FILES = js/jquery-1.11.1.min.js js/json2.js js/jquery.cookie.js js/bootstrap.min.js \
					js/switchery.min.js js/preferences.js
PREFERENCES_JS_ALL = js/preferences-all.js
PREFERENCES_JS_ALL_MIN = js/preferences-all.min.js

ABOUT_CSS_FILES = css/bootstrap.min.css css/bootstrap-theme.css 
ABOUT_CSS_ALL = css/about-all.css
ABOUT_CSS_ALL_MIN = css/about-all.min.css

ABOUT_JS_FILES = js/jquery-1.11.1.min.js  js/bootstrap.min.js
ABOUT_JS_ALL = js/about-all.js
ABOUT_JS_ALL_MIN = js/about-all.min.js


all:	cines-all preferences-all

cines-all: cines-css cines-js
cines-css:  $(CINES_CSS_ALL) $(CINES_CSS_ALL_MIN)
cines-js:  $(CINES_JS_ALL) $(CINES_JS_ALL_MIN)

$(CINES_CSS_ALL):
	rm -f $(CINES_CSS_ALL)
	cat $(CINES_CSS_FILES) > $(CINES_CSS_ALL)

$(CINES_CSS_ALL_MIN):
	rm -f $(CINES_CSS_ALL_MIN)
	$(YUICOMPRESSOR) $(CINES_CSS_ALL) -o $(CINES_CSS_ALL_MIN)


$(CINES_JS_ALL):
	rm -f $(CINES_JS_ALL)
	cat $(CINES_JS_FILES) > $(CINES_JS_ALL)

$(CINES_JS_ALL_MIN):
	rm -f $(CINES_JS_ALL_MIN)
	$(YUICOMPRESSOR) $(CINES_JS_ALL) -o $(CINES_JS_ALL_MIN)



preferences-all: preferences-css preferences-js
preferences-css: $(PREFERENCES_CSS_ALL) $(PREFERENCES_CSS_ALL_MIN)
preferences-js:  $(PREFERENCES_JS_ALL) $(PREFERENCES_JS_ALL_MIN)

$(PREFERENCES_CSS_ALL):
	rm -f $(PREFERENCES_CSS_ALL)
	cat $(PREFERENCES_CSS_FILES) > $(PREFERENCES_CSS_ALL)

$(PREFERENCES_CSS_ALL_MIN):
	rm -f $(PREFERENCES_CSS_ALL_MIN)
	$(YUICOMPRESSOR) $(PREFERENCES_CSS_ALL) -o $(PREFERENCES_CSS_ALL_MIN)

$(PREFERENCES_JS_ALL):
	rm -f $(PREFERENCES_JS_ALL)
	cat $(PREFERENCES_JS_FILES) > $(PREFERENCES_JS_ALL)

$(PREFERENCES_JS_ALL_MIN):
	rm -f $(PREFERENCES_JS_ALL_MIN)
	$(YUICOMPRESSOR) $(PREFERENCES_JS_ALL) -o $(PREFERENCES_JS_ALL_MIN)


about-all:  about-css about-js
about-css:  $(ABOUT_CSS_ALL)  $(ABOUT_CSS_ALL_MIN)
about-js:	$(ABOUT_JS_ALL) $(ABOUT_JS_ALL_MIN)

$(ABOUT_CSS_ALL):
	rm -f $(ABOUT_CSS_ALL)
	cat $(ABOUT_CSS_FILES) > $(ABOUT_CSS_ALL)

$(ABOUT_CSS_ALL_MIN):
	rm -f $(ABOUT_CSS_ALL_MIN)
	$(YUICOMPRESSOR) $(ABOUT_CSS_ALL) -o $(ABOUT_CSS_ALL_MIN)

$(ABOUT_JS_ALL):
	rm -f $(ABOUT_JS_ALL)
	cat $(ABOUT_JS_FILES) > $(ABOUT_JS_ALL)

$(ABOUT_JS_ALL_MIN):
	rm -f $(ABOUT_JS_ALL_MIN)
	$(YUICOMPRESSOR) $(ABOUT_JS_ALL) -o $(ABOUT_JS_ALL_MIN)

clean:  clean-cines clean-preferences

clean-cines:
	rm -f $(CINES_CSS_ALL)
	rm -f $(CINES_CSS_ALL_MIN)
	rm -f $(CINES_JS_ALL)
	rm -f $(CINES_JS_ALL_MIN)

clean-preferences:
	rm -f $(PREFERENCES_CSS_ALL)
	rm -f $(PREFERENCES_CSS_ALL_MIN)
	rm -f $(PREFERENCES_JS_ALL)
	rm -f $(PREFERENCES_JS_ALL_MIN)

clean-about:
	rm -f $(ABOUT_CSS_ALL)
	rm -f $(ABOUT_CSS_ALL_MIN)
	rm -f $(ABOUT_JS_ALL)
	rm -f $(ABOUT_JS_ALL_MIN)


