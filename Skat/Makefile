build:
	docker build -t skat/rust-actix .

run:
	docker run -p 8000:8000 skat/rust-actix

db: 
	createuser -P -s skat_user
	createdb skat_db
	psql -f sql/schema.sql skat_db  
