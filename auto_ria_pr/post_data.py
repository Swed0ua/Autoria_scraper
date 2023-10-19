import requests
import subprocess

URL = ''


def post_request_data (data):
    
    curl_command = f"curl -X POST -d \"regionid={data['regionid']}&phone={data['phone']}&id={data['id']}&name={data['name']}&year={data['year']}&race={data['race']}&price={data['price']}&url={data['url']}&urlimg="+"[{\\\"id\\\":0,\\\"url\\\":\\\""+str(data['img'])+"\\\"}]"+f"&text=<div>{data['desc']}</div>&fio={data['fio']}\" {URL}"

    print(curl_command)
    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode('utf-8'))  # Вивести вміст stdout
    print(stderr.decode('utf-8'))


# post_request_data({
#     'regionid':'6',
#     'phone': '0674730363',
#     'id':'34823035',
#     'name':'VolkswagenID.4',
#     'year':'2023',
#     'race':'1тис.км',
#     'price':'36000',
#     'url':'https://auto.ria.com/uk/auto_volkswagen_id_4_34823035.html',
#     'img':'https://cdn1.riastatic.com/photosnew/auto/photo/volkswagen_id-4__504893821f.jpg',
#     'desc':"n",
#     'fio':'Леон'
# })

