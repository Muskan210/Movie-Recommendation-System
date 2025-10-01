# // run this file on anaconda prompt by going into the file  using cd file name then 
# //run python app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load your data
new = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recs = []
    for i in distances[1:6]:
        recs.append({"title": new.iloc[i[0]].title})
    return recs

@app.route('/recommend')  # <-- THIS is the important part
def recommend_api():
    movie = request.args.get('movie')
    if not movie:
        return jsonify({"error": "No movie provided"}), 400
    try:
        return jsonify({"recommendations": recommend(movie)})
    except:
        return jsonify({"recommendations": []})

if __name__ == '__main__':
    app.run(debug=True)
