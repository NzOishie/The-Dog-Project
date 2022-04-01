from urllib import request

from flask import request
from flask import render_template

from app import app
from utils import get_json_response

config = {
    "DEBUG": True  # run app in debug mode
}


@app.route('/')
def get_dogs():
    """
    renders first ten dogs
    :returns: An HTML page containing a list of dogs with their characteristics
    """
    print("here!in get")
    search_url = ("https://api.thedogapi.com/v1/images/search?"
                  "limit=10&page=1?api_key=234dec54-99a1-4c48-80b0-143c83b93a3a")
    all_dog = get_json_response(search_url)
    return render_template('home.html', dogs=all_dog)


@app.route('/', methods=['POST'])
def get_dogs_post():
    """
    Search for a list of dog for with a given query
    :returns: An HTML page containing a filtered list of dogs
    """
    print("Here!")
    search_query = request.form['text']
    search_url = "https://api.thedogapi.com/v1/breeds/search?q=" + search_query
    dog_list = get_json_response(search_url)

    image_list = []
    for dogs in dog_list:
        image_id = dogs.get("reference_image_id")
        image_list.append(image_id or "")

    images = {}
    for i in image_list:
        if i == '':
            images[i] = ""
        else:
            image_url = "https://api.thedogapi.com/v1/images/" + i
            image_data_json = get_json_response(image_url)
            images[image_data_json['id']] = image_data_json['url']

    for dogs in dog_list:
        image_id = dogs.get("reference_image_id")
        dogs["image_url"] = images[image_id] if image_id else ""
    return render_template('home_search.html', dogs=dog_list)


if __name__ == '__main__':
    app.run(debug=True)
