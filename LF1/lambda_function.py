import json
import boto3
import requests

print('Loading function')

s3 = boto3.client('s3')
rekognition = boto3.client("rekognition")
# open_search = boto3.client("opensearch")

host = 'https://search-photos-swywglfely7rbgh5hv5567ouo4.us-east-1.es.amazonaws.com'
reduced_host = 'search-photos-swywglfely7rbgh5hv5567ouo4.us-east-1.es.amazonaws.com'
region = 'us-east-1'

access_id = 'quantumstatic'
access_secret = 'redacted'

headers = {
    "Content-Type": "application/json"
}

BUCKET_NAME="assbucket2"

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    
    image_name = event['Records'][0]['s3']['object']['key']
    
    if image_name != "newimg.png":
        return
    
    count_file = s3.get_object(
        Key="count.txt",
        Bucket=BUCKET_NAME
    )
        
    curr_count:int = int(count_file["Body"].read().decode("UTF-8"))
    
    s3.put_object(
        Key="count.txt",
        Bucket=BUCKET_NAME,
        Body=str(curr_count+1).encode("utf-8")
    )
    
    copy_source = {
        'Bucket': BUCKET_NAME,
        'Key': "newimg.png"
    }
    
    image_name = f"img{curr_count}.png"
    s3.copy(copy_source, BUCKET_NAME, image_name)
    
    s3.delete_object(Bucket=BUCKET_NAME, Key="newimg.png")
    
    rekognition_response = rekognition.detect_labels(Image = {"S3Object" : {"Bucket": "assbucket2", "Name":image_name}})
    print(rekognition_response)
    
    s3_head_response = s3.head_object(
        Bucket=BUCKET_NAME,
        Key=image_name,
    )
    labels_list = [labelObject["Name"] for labelObject in rekognition_response['Labels']]
    try:
        added_labels = s3_head_response["Metadata"]["customlabels"]
    except KeyError:
        pass
    else:
        labels_list = labels_list + list(map(lambda x: x.strip(), added_labels.split(';')))

    created_time = s3_head_response["LastModified"]
    
    print(labels_list)
    
    elatic_search_obj = {
        'objectKey': image_name,
        'bucket': 'assbucket2',
        'createdTimestamp': str(created_time),
        'labels': labels_list
    }
    
    print(elatic_search_obj)
    
    index_name = 'photos'

    # Document ID
    doc_id = '10'
    
    # url = f"https://{host}/{index_name}/_doc/{doc_id}/{json.dumps(elatic_search_obj)}"
    url = f"{host}/{index_name}/_doc/"
    
    requests_response = requests.post(url, auth=(access_id, access_secret), headers=headers, data=json.dumps(elatic_search_obj))
    
    print(requests_response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
