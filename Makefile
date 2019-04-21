.PHONY: doc test

doc:
	pandoc README.md -o README.pdf

test:
	python3 -m pytest -p no:warnings -v test.py
