
all: hello/hello.cpp
	cd hello && python -c 'from hello import hello; hello()'

hello/hello.cpp:
	./setup.py build

clean:
	rm -rf build dist hello.egg-info hello/hello.cpp
