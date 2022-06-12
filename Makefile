py := python
default_user := dubniczki

# Run with a test user
.PHONY: run
run:
	cd accscout && $(py) main.py dubniczki

# Install package
.PHONY: install
install:
	$(py) setup.py install

# Remove build files
.PHONY: clean
clean:
	rm -rf dist build accscout.egg-info __pycache__

# Count pages in the yaml config
.PHONY: count
count: accscout/pages.yml
	$(py) utils/count.py accscout/pages.yml
