all_upl: wheel sdist upload
all: wheel sdist
wheel:
	pip install -U wheel
	pip install -U setuptools
	pip wheel --no-deps -w dist .

sdist:
	python setup.py sdist

test:
	SBR=sus python3 shenvvt.py 

upload:
	pip install -U twine
	TWINE_USERNAME=$TWINE_USERNAME TWINE_PASSWORD=$TWINE_PASSWORD twine upload dist/*

clean:
	rm -r -f ./build/
	rm -r -f ./*/__pycache__/
	rm -r -f ./*/__pypackages__/
	rm -r -f ./*/*.pyc
	rm -r -f ./build/
	rm -r -f ./*/*.egg-info/
	rm -r -f ./*.egg-info/
	rm -r -f ./dist/