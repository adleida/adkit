develop:
	python setup.py develop

install:
	python setup.py install

test:
	py.test tests/

build:
	python setup.py sdist

upload:
	scp ./dist/tkit-0.0.*.tar.gz python@192.168.1.114:Public/tkit

up_paxp:
	scp python@192.168.1.114:paxp2-0.0.5.tar.gz .
	pip install paxp2-0.0.5.tar.gz
	rm paxp2-0.0.5.tar.gz
