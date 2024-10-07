
PY_FILES = $(wildcard *.py)

run:
	python3 main.py

test: 
	python3 -m unittest ${PY_FILES:.py=}

benchmark: bench
bench:
	python3 bench.py
