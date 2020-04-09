# News Scrapper

This project, has a only endpoint that accept an array of keywords and return 3 news from differents news website.

In this case the soruces used are:

- [El Universal](https://eluniversal.com.mx)
- [La Prensa](https://www.la-prensa.com.mx)
- [La Jornada](https://www.jornada.com.mx)


This server has been allocated in this [url](http://ec2-54-91-202-178.compute-1.amazonaws.com)


## Instalation

You have to enter in the folder

```bash
cd deltaipackage
```
Then execute [docker-compose](https://docs.docker.com/compose/) to create the images
```bash
docker-compose up
````

This process can take a few minutes


The process of the server scrapping from the news website and then save the news in a db with the most relevant tags
for this you have to execute periodically the crawl process

```bash
docker container exec deltaipackage scrapy crawl news
````
You can put this in a crontab

## Usage

##### POST

```
http://localhost:3002/api/news [POST]
```

```
{
    "keywords" : ["amlo", "coronavirus"]
}
```

To test in cloud 

```
http://ec2-54-91-202-178.compute-1.amazonaws.com:3002/api/news [POST]
```
