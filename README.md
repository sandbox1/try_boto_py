## Boto samples of various s3 operations

- create bucket
- upload file
- download file
- delete file 
- copy files between buckets
- list bucket content
- delete buckets 

## Boto Github Project

 ```
 https://github.com/boto/boto3
 ```

## Notes: (As of sept 2016)

If Importing boto3 for use on AWS lamda 
AWS is currently importing boto verion 1.3.1

```
import boto3
def lambda_handler(event, context):
    print(boto3.__version__)
```

## Generating 1.3.1 Documentation

Checkout the 1.3.1 release from github and build docs 

Sphinx is used for documentation. You can generate HTML locally with the following:
```
$ pip install -r requirements-docs.txt
$ cd docs
$ make html
```




