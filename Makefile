.PHONY: all init

all:
	$(MAKE) -C ../GOS_book book

init:
	git submodule update --init --recursive

install:
	cd telegram && python setup.py install
