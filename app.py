from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key="çok gizli bir key"

#veri tabanı bağlantısı
client =MongoClient("mongodb+srv://egitim:egitim48@cluster0-kubck.mongodb.net/test?retryWrites=true&w=majority")

db = client.tododb.todos


@app.route('/')
def index():
    #veri tabanından kayıtlar çek bir listeye al
    yapilacaklar=[]
    for yap in db.find():
        yapilacaklar.append({
            "_id":str(yap.get("_id")),
            "isim":yap.get("isim"),
            "durum":yap.get("durum")
        })
    #index.html by listeyi gönder
    return render_template('index.html',yapilacaklar = yapilacaklar)

@app.route('/guncelle/<id>')
def guncelle(id):
    #id değerinin ilk kaydı
    yap=db.find_one({'_id':ObjectId(id)})
    #true false yapalım
    durum= not yap.get('durum')
    #kaydı güncelle
    db.find_one_and_update(
        {'_id':ObjectId(id)},
        {'$set':{'durum':durum}})


    #ana sayfa yönlendir
    return redirect('/')

@app.route('/sil/<id>')
def sil(id):
    #idsi gelen kaydı sil
    db.find_one_and_delete(
        {'_id':ObjectId(id)})
    #ana sayfaya gönderecez
    return redirect('/')

@app.route('/ekle',methods =['POST'])
def ekle():
    isim=request.form.get('isim')
    db.insert_one({'isim':isim,'durum':'False'})
    return redirect('/')
   
#hatalı yada olmayan bir url isteği gelirse 
#hata vermesin ana sayfaya göndersin
@app.errorhandler(404)
def hatalı_url():
   return redirect('/')

@app.route('/kimiz')
def kimiz():
   return render_template('kimiz.html')

@app.route('/user/<isim>')
def user(isim):
    return render_template('user.html',isim = isim)

if __name__ == '__main__':
  app.run(debug=True)
 