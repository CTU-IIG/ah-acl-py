# Self-documenting Makefile
# Version: s7
# Source: https://github.com/jara001/Makefile
# Originally:
# Self-documenting Makefile by prwhite
# https://gist.github.com/prwhite/8168133
# https://gist.github.com/prwhite/8168133#gistcomment-1716694
# https://gist.github.com/prwhite/8168133#gistcomment-1737630

.PHONY: build develop install uninstall reinstall

help: ## Show this help message.
	@echo "Usage: make [target] ..."
	@echo
	@echo "Targets:"
	@grep --color=auto -F "## " $(MAKEFILE_LIST) | grep --color=auto -F -v grep | sed -e "s/\\$$//" | sed -e "s/##//" | column -c2 -t -s :
	@grep "##@[^ \"]*" $(MAKEFILE_LIST) | grep --color=auto -F -v grep | sed -e "s/^.*##@\\([a-zA-Z][a-zA-Z]*\\).*\$$/\1/" | sed "/^\\$$/d" | sort | uniq | xargs -I'{}' -n 1 bash -c "echo; echo {} targets:; grep '##@{}' $(MAKEFILE_LIST) | sed -e 's/##@{}//' | column -c2 -t -s :"


build: ##@Build Build wheel and wagons.
build: build-wheel build-wagon

build-wheel: ##@Build Build a Python3 wheel.
	python3 setup.py build bdist_wheel --python-tag py3

build-wagon: ##@Build Build a Wagon for each architecture.
	wagon create . --pyver 3 --supported-platform manylinux2014_x86_64
	wagon create . --pyver 3 --supported-platform manylinux2014_aarch64
	wagon create . --pyver 3 --supported-platform manylinux2014_armv7l

develop: ##@Developer Install the package as link to this repository.
	python3 setup.py develop --user

install: ##@Install Install the package for current user.
	python3 setup.py install --user

uninstall: ##@Install Uninstall the package.
	python3 -m pip uninstall '$(notdir $(CURDIR))'

reinstall: ##@Install Reinstall the package
reinstall: uninstall install

test: ##@Test Run the unit tests.
	python3 -m unittest discover -s tests
