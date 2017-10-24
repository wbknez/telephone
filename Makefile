# Makefile for Telephone.

init:
	pip install -r requirements.txt --user

run:
	@ python3 -m telephone.main

test:
	@ python3 -m nose2
