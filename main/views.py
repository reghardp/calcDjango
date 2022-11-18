from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import string, random
import time
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here. 

# def index(response):
#     return render(response, "main/base.html", {})

# def home(response):
#     return render(response, "main/base.html") 

# def home(response):
#     return render(response, "base.html") 

# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'base.html', { 
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'base.html') 

account = "autopricing"   # Azure account name
key = "z+hBvJzSDUokiPxKfiSbxcWdMwgtG0ftlcZubzvl3TzXzYX+SDe8JDA1ypboL0fcFrxPp+vpJSR6+AStdT+4Fw=="     # Azure Storage account access key  
container = "excel-input" # Container name
url = "https://autopricing.blob.core.windows.net"
conn_string = 'DefaultEndpointsProtocol=https;AccountName=autopricing;AccountKey=z+hBvJzSDUokiPxKfiSbxcWdMwgtG0ftlcZubzvl3TzXzYX+SDe8JDA1ypboL0fcFrxPp+vpJSR6+AStdT+4Fw==;EndpointSuffix=core.windows.net'
conn_stringOUT = 'DefaultEndpointsProtocol=https;AccountName=exportdata23;AccountKey=rbVxBcL3cGi7FBl5Jj0EacsDzGZ9GiFikGzMQeF6BPyyW3rrPLiJXW82M4s21iJDC0+66l2Ywsim+AStwj3KDA==;EndpointSuffix=core.windows.net'

blob_service = BlobServiceClient.from_connection_string(conn_string)
blob_serviceOUT = BlobServiceClient.from_connection_string(conn_stringOUT)
# blob_service = BlobServiceClient(account_name=account, account_key=key, account_url=url)
# cnt_settings = ContentSettings(content_type=)
# blob_client =  BlobClient.from

# with open(SOURCE_FILE, "rb") as data:
#     blob_client.upload_blob(data, blob_type="BlockBlob")

def home(response):
    if response.method == 'POST' and response.FILES['myfile']:
        myfile1 = response.FILES['myfile']
        fs = FileSystemStorage()
        file_name = fs.save(myfile1.name, myfile1)
        # fileextension = 'txt'
        fileextension = file_name.rsplit('.',1)[1]
        Randomfilename = id_generator()
        filename = Randomfilename + '.' + fileextension
        uploaded_file_url = 'https://exportdata23.blob.core.windows.net/out/' + filename
        # uploaded_file_url = fs.url(filename)
        # blob_service.create_blob_from_stream(container, filename, myfile)
        # blob_client = blob_service.get_blob_client(container=container, blob=filename)
        # data = "test"
        # blob_client = blob_service.get_blob_client(container=container, blob=filename)
        # blob_client.upload_blob(data)
        with open(file_name, 'rb') as data:
            blob_client = blob_service.get_blob_client(container=container, blob=filename)
            blob_client.upload_blob(data)
        # blob_client.upload_blob(myfile1)
        for i in range(20):
            done = ifblob_exists(filename)
            if done:
                print("\t Blob exists :" + " " + filename)
                return render(response, 'base.html', {
                    'uploaded_file_url': uploaded_file_url
                }) 
            else:
                print("\t Blob does not exists :" + " " + filename)
                time.sleep(7)

        # return render(response, 'base.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
    return render(response, 'base.html')    

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  
def ifblob_exists(filename):
   try:
      container_name = 'out'
    #   block_blob_service = BlockBlobService(account_name='exportdata23', account_key='rbVxBcL3cGi7FBl5Jj0EacsDzGZ9GiFikGzMQeF6BPyyW3rrPLiJXW82M4s21iJDC0+66l2Ywsim+AStwj3KDA==', socket_timeout=60)
      blob_clientOUT = blob_serviceOUT.get_blob_client(container='out', blob=filename)
      isExist = blob_clientOUT.exists()
      if isExist: 
         return True
      else:
         return False
   except Exception:
      print('Not found')    
 