# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* opti_recruit/*.py

black:
	@black scripts/* opti_recruit/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr opti_recruit-*.dist-info
	@rm -fr opti_recruit.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

download_fbref:
	@rm -rf app/assets/stylesheets
	@curl -L https://github.com/riadh-anis/opti_recruit/hbref_scraped_data.zip > hbref_scraped_data.zip
	@unzip hbref_scraped_data.zip -d raw_data/fbref && rm hbref_scraped_data.zip && mv fbref_2017.csv raw_data/fbref && mv fbref_2018.csv raw_data/fbref && mv fbref_2019.csv raw_data/fbref && mv fbref_2020.csv raw_data/fbref && mv fbref_2021.csv raw_data/fbref && mv fbref_2022.csv raw_data/fbref && mv fbref_2023.csv raw_data/fbref && mv fbref_2024.csv raw_data/fbref && mv fbref_2025.csv raw_data/fbref && mv fbref_2026.csv raw_data/fbref && mv fbref_2027.csv raw_data/fbref && mv fbref_2028.csv raw_data/fbref && mv fbref_2029.csv raw_data/fbref && mv fbref_2030.csv raw_data/fbref && mv fbref_2031.csv raw_data/fbref && mv fbref_2032.csv raw_data/fbref && mv fbref_2033.csv raw_data/fbref && mv fbref_2034.csv raw_data/fbref && mv fbref_2035.csv raw_data/fbref && mv fbref_2036.csv raw_data/fbref && mv fbref_2037.csv raw_data/fbref && mv fbref_2038.csv raw_data/fbref && mv fbref_2039.csv raw_data/fbref && mv fbref_2040.csv raw_data/fbref && mv fbref_2041.csv raw_data/fbref && mv fbref_2042.csv raw_data/fbref && mv fbref_2043.csv raw_data/fbref && mv fbref_2044.csv raw_data/fbref && mv fbref_2045.csv raw_data/fbref && mv fbref_2046.csv raw_data/fbref && mv fbref_2047.csv raw_data/fbref && mv fbref_2048.csv raw_data
