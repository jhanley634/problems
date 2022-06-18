
TEMP = /tmp/loadtxt.d
OBJ = rust_lib/target/debug/librust.dylib

OUT = \
 $(TEMP) \
 $(OBJ) \

all: $(OUT)

$(TEMP):
	./generate.py $@

$(OBJ): rust_lib/src/lib.rs
	cd rust_lib && maturin develop && env RUST_BACKTRACE=1 ./load_2.py

clean:
	rm -rf $(OUT) rust_lib/Cargo.lock rust_lib/target
