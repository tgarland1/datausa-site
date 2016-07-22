# Data USA
The most comprehensive visualization of U.S. public data

To run a local copy of this site on your machine, create a Ubuntu VM and follow: 

1.	sudo apt install git python python-dev python-pip postgresql postgresql-contrib libpq-dev libjpeg8-dev virtualenv
2.	mkdir sites
3.	cd sites/
4.	git clone https://github.com/tgarland1/datausa-site.git
5.	virtualenv datausa
6.	source datausa/bin/activate
7.	cd datausa-site/
8.	pip install –r requirements.txt
9.	python run.py gunicorn
10.	navigate to http://127.0.0.1:8000 in your browser
