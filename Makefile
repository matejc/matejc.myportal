# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python
options =

all: docs tests

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/matejc/myportal/*.py src/matejc/myportal/browser/*.py src/matejc/myportal/tests/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg buildout.d/*.cfg setup.py
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py
	@touch $@

$(python):
	virtualenv -p python$(version) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/flake8 src/matejc/myportal
	@for pt in `find src/matejc/myportal -name "*.pt"` ; do bin/zptlint $$pt; done
	@for xml in `find src/matejc/myportal -name "*.xml"` ; do bin/zptlint $$xml; done
	@for zcml in `find src/matejc/myportal -name "*.zcml"` ; do bin/zptlint $$zcml; done

clean:
	@rm -rf .installed.cfg .mr.developer.cfg bin docs/html parts develop-eggs \
		src/matejc.myportal.egg-info lib include .Python

.PHONY: all docs tests clean
