# access-pc

Access'PC Website

## Configure

Refers to `res/config_default.ini` and make your own `config.ini`

/!\ Database :

- MariaDB / MySQL required
- User / Pass that have access to database

## Docker deploy

Download and config config_default.ini then:  
`docker run -it -p 8080:8080 -v $(pwd)/res/config.ini:/home/access-pc/res/config.ini apresse/api-test`
