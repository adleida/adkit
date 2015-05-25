develop:
	python setup.py develop

install:
	python setup.py install

test:
	py.test tests/

build:
	python setup.py sdist

upload: build
	scp ./dist/adkit-0.0.9.2.tar.gz 114:
	scp ./dist/adkit-0.0.9.2.tar.gz ali:
