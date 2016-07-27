# TODO: Replace with project name
PROJECT_NAME = project_name
STATIC_LIBS_DIR = ./$(PROJECT_NAME)/static/libs

LESS_VERSION = 2.1.0
MODERNIZR_VERSION = 2.8.3
JQUERY_VERSION = 1.11.2
BOOTSTRAP_VERSION = 3.3.1

default: lint test

test:
	# Run all tests and report coverage
	# Requires coverage
	coverage run manage.py test
	coverage report -m --fail-under 63

lint-py:
	# Check for Python formatting issues
	# Requires flake8
	flake8 .

lint-js:
	# Check JS for any problems
	# Requires jshint
	find -name "*.js" -not -path "${STATIC_LIBS_DIR}*" -print0 | xargs -0 jshint

lint: lint-py lint-js

$(STATIC_LIBS_DIR):
	mkdir -p $@

$(STATIC_LIBS_DIR)/less.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/less.js/$(LESS_VERSION)/less.js -O $@

LIBS := $(STATIC_LIBS_DIR)/less.js

$(STATIC_LIBS_DIR)/modernizr.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/modernizr/$(MODERNIZR_VERSION)/modernizr.js -O $@

LIBS += $(STATIC_LIBS_DIR)/modernizr.js

$(STATIC_LIBS_DIR)/jquery.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/jquery/$(JQUERY_VERSION)/jquery.js -O $@

LIBS += $(STATIC_LIBS_DIR)/jquery.js

$(STATIC_LIBS_DIR)/bootstrap: $(STATIC_LIBS_DIR)
	wget https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP_VERSION}/bootstrap-${BOOTSTRAP_VERSION}-dist.zip -O bootstrap.zip
	unzip bootstrap.zip
	mv dist $@
	rm bootstrap.zip

LIBS += $(STATIC_LIBS_DIR)/bootstrap

update-static-libs: $(LIBS)

# OS := $(shell uname)
# ifeq ($(OS), Darwin)
# 	@cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w $(length) | head -n 1 | tr -d '\n'; echo
# else
# 	@strings /dev/urandom | grep -o '[[:alnum:]]' | head -n $(length) | tr -d '\n'; echo
# endif
# Generate a random string of desired length
generate-secret: length = 32
generate-secret:
	@cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w $(length) | head -n 1 | tr -d '\n'; echo

conf/%.pub.ssh:
	# Generate SSH deploy key for a given environment
	ssh-keygen -t rsa -b 4096 -f $*.priv -C "$*@${PROJECT_NAME}"
	@mv $*.priv.pub $@

staging-deploy-key: conf/staging.pub.ssh

production-deploy-key: conf/production.pub.ssh

.PHONY: default test lint lint-py lint-js generate-secret

.PRECIOUS: conf/%.pub.ssh
