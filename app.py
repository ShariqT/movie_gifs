from flask import Flask, render_template, request, make_response
import json, pprint
import requests as urlRequest
TUMBLR_KEY = "DM8c5b9mvlHsaJrRHBYwKtxAUI8ajzNYPinzdhqn3lBgoZIy6t"
TUMBRL_API = "https://api.tumblr.com/v2/"
ROTTEN_TOMATO_KEY = "8d919e9368fe04efabad7611d4f9d706"
ROTTEN_TOMATO_API = "https://api.themoviedb.org/3"
app = Flask(__name__)


def loop_media(media, container):
	for m in media:
		pprint.pprint(m['original_size']['url'][-3:])
		if(m['original_size']['url'][-3:] == "gif"):
			container.append(m['original_size']['url'])
	return container

def create_chunks(container, num):
	n = max(1, num)
	return [container[i:i + n] for i in range(0, len(container), n)]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/tumblr/get_tagged", methods=["GET",])
def search_tumblr():
	res = urlRequest.get(TUMBRL_API + "tagged", {"api_key": TUMBLR_KEY, "tag": request.args.get('q')})
	
	raw_response = res.json()
	if raw_response['meta']['status'] != 200:
		return_data = json.dumps({"error": "There was an issue contacting the Tumblr API. We will not be able to load gifs :("})
		resp = make_response(return_data, 500)
		resp.headers["Content-Type"] = "application/json"
		return resp

	return_list = []
	for post in raw_response['response']:
		if "photos" in post:
			loop_media(post['photos'], return_list)
	return_list = create_chunks(return_list, 2)
	resp = make_response(json.dumps({"gifs": return_list}), 200)
	resp.headers['Content-Type'] = 'applicaton/json'
	return resp

@app.route("/api/rotten/movie", methods=["GET",])
def search_rt():
	res = urlRequest.get(ROTTEN_TOMATO_API + "/search/movie", {'api_key': ROTTEN_TOMATO_KEY, 'query': request.args.get('q'), 'page_limit': 1, 'page': 1})
	raw_response = res.json()
	if res.status_code != 200:
		return_data = json.dumps({"error": "There was an issue contacting the Rotten Tomato API. Will not be able to load movie info :("})
		resp = make_response(return_data, 500)
		resp.headers['Content-Type'] = 'application/json'
		return resp

	return_list = []
	pprint.pprint(raw_response)
	resp = make_response(json.dumps({"movies":raw_response['results']}))
	resp.headers['Content-Type'] = 'application/json'
	return resp

if __name__ == "__main__":
	app.debug = True
	app.run()