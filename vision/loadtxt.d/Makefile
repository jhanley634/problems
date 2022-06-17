
TEMP = /tmp/loadtxt.d

OUT = \
 $(TEMP) \
 rust_lib/target/release/librust_lib.rlib \

all: $(OUT)

$(TEMP):
	./generate.py $@

rust_lib/target/release/librust_lib.rlib: rust_lib/src/lib.rs
	cd rust_lib && cargo build --release && ./load_2.py
