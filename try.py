import boto3
import os
objectKey = 'hworld.txt'
bucketNameInput = 'beachbucket'
localFilename = '/tmp/{}'.format(os.path.basename(objectKey))
s3 = boto3.client('s3')
s3.download_file(bucketNameInput,objectKey,localFilename)
print localFilename
print(open(localFilename).read())
print 'EOF'