.PHONY: all init

all:
	$(MAKE) -C ../GOS_book book

init:
	git submodule update --init --recursive

setup: init
	cd telegram && python setup.py install
	cd tarantool-python && python setup.py install
