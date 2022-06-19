
# Copyright 2022 John Hanley. MIT licensed.

TEMP = /tmp/loadtxt.d
OBJ = rust_lib/target/release/librust_fast.dylib

OUT = \
 $(TEMP) \
 $(OBJ) \

all: $(OUT)

$(TEMP):
	./generate.py $@

RUN = env RUST_BACKTRACE=1 ./load_2.py

$(OBJ): rust_lib/src/lib.rs
	cd rust_lib && maturin develop --release && $(RUN)

run: $(OBJ)
	cd rust_lib && $(RUN)
	./load_1.py

clean:
	rm -rf $(OUT) rust_lib/Cargo.lock rust_lib/target
