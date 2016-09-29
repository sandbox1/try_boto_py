import boto3
import os
import json

with open('./env.json') as env_file:
    config = json.load(env_file)
for key, value in config.items():
    os.environ[key] = str(value)

s3 = boto3.resource('s3')

# http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.create_bucket
def createBucket(bucketname):    
    bucket = s3.create_bucket(Bucket=bucketname)
    print 'Created bucket {} '.format(bucket.name)   
    return bucket
     

def uploadFile(file,bucket):
    print 'Uploading {} '.format(file.name)
    bucket.upload_fileobj(file,file.name)
    print 'Upload complete'    


def downloadFile(filename,bucket,localfilePath):
    print "Downloading {} from {} to {} ".format(filename, bucket.name, localfilePath) 
    bucket.download_file(filename,localfilePath)
    print "Download complete"


def copyFile(srcBucket,srcKey, destBucket, destKey):
    print 'Server copy of {} from bucket {} to bucket{} '.format( srcKey, srcBucket.name, destBucket.name)
    copy_source = {
        'Bucket':srcBucket.name,
        'Key':srcKey
    }
    print 'Server copy complete'
    return destBucket.copy(copy_source,destKey)

def listFiles( bucket ):
    print 'List Files in bucket {} '.format( bucket.name )
    for key in bucket.objects.all():
        print('...{}'.format(key.key))    


def deleteFile(bucket,filename):
    print 'Delete File {} from bucket {}'.format( filename, bucket.name )
    DeleteDict = {
        'Objects':[{
            'Key':filename
        }]
    }
    bucket.delete_objects( Delete=DeleteDict )


def delBucketContent(bucket):
    print 'Deleting bucket content'
    for key in bucket.objects.all():
        print'....{}'.format(key)
        key.delete()


def delBucket(bucket):
    print 'Delete bucket {} '.format( bucket.name )
    delBucketContent(bucket)
    bucket.delete()
    print 'Bucket deleted'
    


def moveFile(srcBucket,srcFile, destBucket, destFile):
    print 'Moving file {} '.format( srcFile)
    copyFile(srcBucket,srcFile,destBucket,destFile)
    deleteFile(srcBucket,srcFile)
    

# Create Bucket
sourceBucket = createBucket(os.environ['sourceBucketName'])
destBucket = createBucket(os.environ['destBucketName'])
print ''

# Upload file to source bucket
uploadFileObj = open( os.environ['uploadFilename'])
uploadFile(uploadFileObj, sourceBucket)
print ''

# Download file from the source bucket
downloadFilePath = os.path.join(os.path.curdir,os.environ['downloadFilename'])
downloadFile(uploadFileObj.name,sourceBucket,downloadFilePath)
print ''

# Perform a 'server side' copy of the uploaded file
copyResponse = copyFile(sourceBucket,uploadFileObj.name, destBucket, os.environ['copyFilename'])
print ''

# list bucket items
listFiles(destBucket)
listFiles(sourceBucket)
print ''

# Move the copied item from dest back to source keeping the same name(Copy with a Delete)
moveFile(destBucket,os.environ['copyFilename'],sourceBucket,os.environ['copyFilename'])
print ''

# list bucket items to see results of the move
listFiles(destBucket)
listFiles(sourceBucket)
print ''

# Delete the moved item from the source
deleteFile(sourceBucket,os.environ['copyFilename'])
print ''

listFiles(destBucket)
listFiles(sourceBucket)
print ''

# Delete buckets
# All of the keys in a bucket must be deleted before the bucket itself can be deleted
delBucket(sourceBucket)
print ''
delBucket(destBucket)
print ''

print 'EOF'
