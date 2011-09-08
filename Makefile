all: deps test

deps:

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install --no-deps specloud -r http://github.com/hugobr/specloud/raw/master/requirements.txt

should-dsl:
	@python -c 'import should_dsl' 2>/dev/null || pip install http://github.com/hugobr/should-dsl/tarball/master

coverage_py:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

test_deps: specloud should-dsl coverage_py

coverage: test_deps
	@nosetests spec/*.py -s --with-coverage --cover-erase --cover-inclusive --cover-package=fluidity

test: test_deps unit

unit:
	@echo =======================================
	@echo ========= Running unit specs ==========
	@specloud spec
	@echo

