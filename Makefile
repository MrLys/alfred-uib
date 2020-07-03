all:
	cd src ; \
	zip ../uib-for-alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc* --exclude=__pycache__

clean:
	rm -f *.alfredworkflow
