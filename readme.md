# How to use

Install dependencies:

`pipenv install` or `pip install -r requirements.txt`

Run redis container:

`docker run -p 6379:6379 -d redis:3.2`


## Google Cloud Translation

Generate service account key:

https://cloud.google.com/docs/authentication/getting-started

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials"
```