
SHELL := bash
ACTIVATE := source .venv/bin/activate

all:
	ls -l

.venv:
	uv venv --python=python3.13

install: .venv
	sort -o requirements.txt{,}
	$(ACTIVATE) && uv pip install --upgrade -r requirements.txt

run: .venv
	$(ACTIVATE) && ./cart_pole.py

clean:
	rm -rf .venv
