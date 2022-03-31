from urllib import request

from flask import Flask, request
from flask import render_template
import  urllib,json
import ssl
import certifi

config = {
    "DEBUG": True  # run app in debug mode
}
app = Flask(__name__)


@app.route('/')
# def hello_world():  # put application's code here
#     return "Hello World"

@app.route('/')
def get_dogs():  # put application's code here
    url = "https://api.thedogapi.com/v1/images/search?limit=10&page=1?api_key=234dec54-99a1-4c48-80b0-143c83b93a3a"
    response = urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    data = response.read()
    dict = json.loads(data)
    return render_template('home.html', dogs = dict)

@app.route('/', methods = ['POST'])
def get_dogs_post():
    q = request.form['text']
    url = "https://api.thedogapi.com/v1/breeds/search?q="+q
    response = urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    data = response.read()
    list = json.loads(data)
    image_list = []

    for dogs in list:
        image_id = dogs.get("reference_image_id")
        if image_id:
            image_list.append(image_id)
        else:
            image_list.append("")


    images = {}
    for i in image_list:
        if i == '':
            images[i] = ""
        else:
            image_url = "https://api.thedogapi.com/v1/images/"+i
            image_response = urllib.request.urlopen(image_url, context=ssl.create_default_context(cafile=certifi.where()))
            image_data = image_response.read()
            image_data_json = json.loads(image_data)
            images[image_data_json['id']] =  image_data_json['url']


    for dogs in list:
        image_id = dogs.get("reference_image_id")
        if image_id:
            dogs["image_url"] = images[image_id]
        else:
            dogs["image_url"] = ""


    print(images)
    print(list)
    return render_template('home_search.html', dogs=list)

if __name__ == '__main__':
    app.run(debug=True)
