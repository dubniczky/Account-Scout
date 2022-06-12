py := python
default_user := dubniczki

# Run with a test user
.PHONY: run
run:
	$(py) accscout/ dubniczki

# Install package
.PHONY: install
install:
	$(py) setup.py install

# Remove build files
.PHONY: clean
clean:
	rm -rf dist build accscout.egg-info __pycache__