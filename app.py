from flask import Flask, jsonify, request, Response, render_template,redirect, url_for
from database.db import initialize_db
from database.models import Video

import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS']={
    #docker
    #'host':'mongodb://127.0.0.1:27017/videos_api'
    #cloud.mongodb
    "host":"mongodb+srv://thales1234:thales12345@cluster0.phfwc.mongodb.net/videoapi?retryWrites=true&w=majority"
}



initialize_db(app)

check_list = lambda value, list_values : [True if l['theme'] == value else False for l in list_values] 


@app.route('/')
def root():
    #return 'OK', 200
    return render_template('index.html')

#get all videos
@app.route('/videos')
def getAll_video():
    videos = Video.objects().to_json()
    #print(videos)
    #return Response(videos, mimetype="application/json", status=200)
    return render_template('list.html', titulo='Videos', videos = json.loads(videos))

#add video
@app.route('/create', methods=['POST'])
def create():
    #body=request.get_json()
    #video = Video(**body).save()
    #id = video.id
    #return {'id':str(id)}, 200
    
    new_obj = {'name' : request. form['name'], 'theme': request.form['theme']}
    Video(**new_obj).save()
    return redirect(url_for('root'))

#route for a new_page render
@app.route('/video')
def add_video():
    return render_template('new_video.html', titulo='New Video')

#get video by id
@app.route('/videoid/<id>')
def get_videoid(id):
    video = Video.objects.get(id=id).to_json()
    return Response(video, mimetype="application/json", status=200)

#update like
@app.route('/like/<id>')
def get_like(id):
    Video.objects(id=id).update_one(inc__like=1)
    #return 'ok', 200
    return redirect(url_for('getAll_video'))


#update dislike
@app.route('/dislike/<id>')
def get_deslike(id):
    Video.objects(id=id).update_one(inc__dislike=1)
    #return 'ok', 200
    return redirect(url_for('getAll_video'))

#themes and like e dislike
@app.route('/themes')
def get_themes():
    theme_list = []
    video_list = Video.objects().to_json()
    for t in json.loads(video_list):
        if theme_list == []:
            theme_list.append({'theme' : t['theme'], 'likes': 0, 'dislikes': 0, 'score':0})
        else:
            aux = True
            for th in theme_list:
                if th['theme'] == t['theme']:
                    th['likes']+=t['like']
                    th['dislikes']+=t['dislike']
                    th['score'] = th['likes']-(th['dislikes']/2)   
                    aux=False
            if aux:
                theme_list.append({'theme' : t['theme'], 'likes': 0, 'dislikes': 0, 'score':0})
    
    #theme_list_ordened = sorted(theme_list, key=lambda th: th['score'], reverse=True)
    theme_list = sorted(theme_list, key=lambda th: th['score'], reverse=True)
    
    #return Response(json.dumps(theme_list), mimetype="application/json", status=200)
    return render_template('themes.html', titulo='Score of Themes', theme_list = theme_list)

if __name__=='__main__':
    app.run(threaded=True, port=5000)
    #app.run(debug=True, use_reloader=True)