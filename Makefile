.PHONY: release dist test lint coverage clean

release: dist
	git tag -a v`python -c 'import httpexceptor; print httpexceptor.__version__'`
	git push origin master --tags

dist: clean test
	rm -r dist || true
	python setup.py sdist

test: clean
	py.test -s --tb=short test

lint:
	find . -name "*.py" -not -path "./venv/*" | while read filepath; do \
		pep8 --ignore=E128,E261 $$filepath; \
	done
	#upyflakes $$filepath; \
	#pylint --reports=n --include-ids=y $$filepath; \

coverage: clean
	# option #1: figleaf
	find httpexceptor test -name "*.py" > coverage.lst
	figleaf `which py.test` test
	figleaf2html -f coverage.lst
	# option #2: coverage
	coverage run `which py.test` test
	coverage html
	# reports
	coverage report
	@echo "[INFO] additional reports in \`html/index.html\` (figleaf) and" \
			"\`htmlcov/index.html\` (coverage)"

clean:
	find . -name "*.pyc" | xargs rm || true
	rm -rf html .figleaf coverage.lst # figleaf
	rm -rf htmlcov .coverage # coverage
	rm -rf test/__pycache__ # pytest
	rm -r httpexceptor.egg-info || true
