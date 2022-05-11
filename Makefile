all_upl: bdist_wheel sdist build_py rotate upload
all: bdist_wheel sdist build_py rotate

runfromsource: deps
	python3 -m cc-secure.server

deps:
	pip install -r ./requirements.txt

bdist_wheel:
	pip install -U wheel
	pip install -U setuptools
	python3 setup.py --verbose bdist_wheel

sdist:
	python setup.py sdist

build_py:
	python3 setup.py build_py

upload:
	pip install -U twine
	twine upload --verbose dist/*

rotate:
	python3 setup.py rotate

clean:
	@echo Deleting dists and run files
	rm -r -f build/
	rm -r -f */*/__pycache__/
	rm -r -f */__pycache__/
	rm -r -f */__pypackages__/
	rm -r -f */*.pyc
	rm -r -f build/
	rm -r -f */*.egg-info/
	rm -r -f *.egg-info/
	rm -r -f dist/