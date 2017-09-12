help:
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with pylnt"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	pylint app/

test:
	py.test tests