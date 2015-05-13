develop:
	python setup.py develop

install:
	python setup.py install

test:
	py.test tests/

build:
	python setup.py sdist

upload: build
	scp ./dist/adkit-0.0.4.tar.gz python@192.168.1.114:/tmp
