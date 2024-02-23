
SHELL := bash

PROG := '...;\
  from foo.bar import baz_1; \
  from foo.qux import yyz_2; \
  print(baz_1 + yyz_2)'

QUX = /tmp/two/foo/qux.py

all: $(QUX)
	env PYTHONPATH=.:/tmp/one:/tmp/two  python -c $(PROG)

$(QUX): clean
	mkdir -p /tmp/{one,two}/foo
	echo baz_1 = 1 > /tmp/one/foo/bar.py
	echo yyz_2 = 2 > $(QUX)

clean:
	rm -rf /tmp/{one,two}
