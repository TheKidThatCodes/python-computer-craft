all_upl: wheel sdist upload
all: wheel sdist

runfromsource: deps
	python3 -m cc-secure.server

deps:
	pip install -r ./requirements.txt

wheel:
	pip install -U wheel
	pip install -U setuptools
	python3 setup.py --verbose bdist_wheel

sdist:
	python setup.py sdist

upload:
	pip install -U twine
	twine upload --verbose dist/*

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