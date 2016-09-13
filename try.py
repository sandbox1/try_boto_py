import boto3
import os
objectKey = 'hworld.txt'
bucketNameInput = 'beachbucket'
localFilename = '/tmp/{}'.format(os.path.basename(objectKey))

s3 = boto3.resource('s3')
inputBucket = s3.Bucket(bucketNameInput)
inputBucket.download_file(objectKey,localFilename)
print localFilename
print(open(localFilename).read())
print 'EOF'