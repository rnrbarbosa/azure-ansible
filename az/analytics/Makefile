all: build test

build:
	ansible-galaxy collection build -f -vv
	ansible-galaxy collection install -f az-analytics-1.0.0.tar.gz

test:
	ansible-playbook tests/test.yml -v

clean:
	rm *.tar.gz