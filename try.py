import boto3
import os
objectKey = 'hworld.txt'
sourceBucketName = 'SourceBucket'
destBucketName = 'DestBucket'
localFilename = '/tmp/{}'.format(os.path.basename(objectKey))
s3 = boto3.resource('s3')
sourceBucket = s3.Bucket(sourceBucketName)
sourceBucket.download_file(objectKey,localFilename)
#do some local processing...
destBucket = s3.Bucket(destBucketName)
destObjectKey = destBucket.Object(objectKey)
with open(localFilename,'rb') as data:
    destObjectKey.upload_fileobj(data)
    print 'Upload to to dest bucket'

print 'EOF'