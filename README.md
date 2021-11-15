# access-pc

Access'PC Website

## Docker deploy

Download and config config_default.ini then:
`docker run -it -p 8080:8080 -v $(pwd)/res/config.ini:/home/access-pc/res/config.ini apresse/api-test`
