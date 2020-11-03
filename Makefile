cmd = cd src; pipenv run
docker_cmd = docker-compose run --rm python

.PHONY : run
run :
	$(cmd) start

.PHONY : lint
lint :
	$(cmd) pycodestyle *.py --show-source

.PHONY : pylint
pylint :
	$(cmd) pylint *.py

.PHONY : typecheck
typecheck :
	$(cmd) typecheck

.PHONY : before_test
before_test :
	bash before_test.sh

.PHONY : test
test :
	@echo "Generate Testdata..."
	@make before_test >> /dev/null 2>&1
	$(cmd) test
	$(cmd) report

.PHONY : clean
clean :
	echo WIP
