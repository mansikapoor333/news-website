from flask import Flask, request, jsonify, send_from_directory
# from flask-cors import CORS, cross_origin
import re
import collections
from newsapi import NewsApiClient
# from newsapi.newsapi_exception import NewsAPIException

application = Flask(__name__, static_url_path='', static_folder='static')

@application.route('/')
def root():
    # print('hello')

    return send_from_directory('static','index1.html')

@application.route('/saw', methods = ['GET'])
def index():
    # head_now = request.args.get('query')
    newsapi = NewsApiClient(api_key="34a75cc37de44563acd6cfd166285520")
    top_headlines = newsapi.get_top_headlines(q='',
                                              sources='fox-news',
                                              # domains='News.com.au',
                                              # from_param='2020-02-01',
                                              # to='2020-02-12',
                                              # category='business',
                                              language='en',
                                              # sort_by='publishedAt',
                                               page_size=30)

                                              # country='us')
# fox news
    abc = top_headlines
    if "articles" in abc:
        listwar = abc["articles"]
        bad = []
    for d in listwar:
        for key, value in d.items():
            if key == 'content':
                continue

            if key == 'source':
                x = value
                if x['id'] is None or x['name'] is None:
                    bad.append(d)
                    break

            if not value:
                bad.append(d)
                break

    for x in bad:
        listwar.remove(x)
    kaj = listwar[:4]

    qwer = {}
    qwer['key'] = kaj
# all news
    gen = newsapi.get_top_headlines(language='en', country='us', page_size=30)

    news = gen['articles']
    bd = []
    for k in news:
        for key, value in k.items():
            if key == 'content':
                continue

            if key == 'source':
                x = value
                if x['id'] is None or x['name'] is None:
                    bd.append(k)
                    break

            if not value:
                bd.append(k)
                break

    for y in bd:
        news.remove(y)
    jkl = news[:5]

    qwer['gen'] = jkl

# cnn news
    cnews = newsapi.get_top_headlines(language='en', sources='cnn', page_size=30)

    newsforcnn = cnews['articles']
    badcnn = []
    for z in newsforcnn:
        for key, value in z.items():
            if key == 'content':
                continue

            if key == 'source':
                x = value
                if x['id'] is None or x['name'] is None:
                    badcnn.append(z)
                    break

            if not value:
                badcnn.append(z)
                break

    for w in badcnn:
        newsforcnn.remove(w)
    mno = newsforcnn[:4]

    qwer['cnews'] = mno

    return jsonify(qwer)    

  


@application.route('/queryget', methods=['GET'])
def get_query():
    newsapi = NewsApiClient(api_key="34a75cc37de44563acd6cfd166285520")
    query_now = request.args.get('query')
    source_now = request.args.get('sources')
    from_now = request.args.get('from_param')
    to_now = request.args.get('to')
    cat_now = request.args.get('category')
    err = dict()


    if (cat_now == 'all'):
        diction={}
        print(from_now + ' ' + to_now)
        try:
            sour = newsapi.get_everything(q=query_now,
                                       sources='',
                                              from_param=from_now,
                                              to=to_now,
                                              language='en',
                                              # country='us',
                                              sort_by='publishedAt',
                                               page_size=30)
        except Exception as e:
            # print(e)
            #error = dict()
            # print('i am here')
            # print(str(e))
            err['message'] = str(e)
            return jsonify(e.__dict__)

        sourfor = sour['articles']
        badnews = []
        for z in sourfor:
            for key, value in z.items():
                if key == 'content':
                    continue

                if key == 'source':
                    x = value
                    if x['id'] is None or x['name'] is None:
                        badnews.append(z)
                        break

                if not value:
                    badnews.append(z)
                    break

        for w in badnews:
            sourfor.remove(w)
        mno = sourfor[:10]

        diction['sour'] = mno
        print(diction)


        return jsonify(diction)


    if (cat_now != 'all' and source_now !='all'):
        hel = {}
        try:
            all_sources = newsapi.get_sources(category=cat_now, country='us', language='en')
            all_str = ','.join(all_sources)

            mat = newsapi.get_everything(q=query_now,
                                         sources=source_now,
                                         from_param=from_now,
                                         to=to_now,
                                         language='en',
                                         sort_by='publishedAt',
                                         page_size=30)
        except Exception as e:
            err['message'] = str(e)
            return jsonify(e.__dict__)

        matfor = mat['articles']
        badnews = []
        for z in matfor:
            for key, value in z.items():
                if key == 'content':
                    continue

                if key == 'source':
                    x = value
                    if x['id'] is None or x['name'] is None:
                        badnews.append(z)
                        break

                if not value:
                    badnews.append(z)
                    break

        for w in badnews:
            matfor.remove(w)
        mno = matfor[:10]
        print(len(mno))

        hel['all_sources'] = mno
        print(hel)

        return jsonify(hel)




    if (cat_now!='all' and source_now == 'all'):
        god={}
        try:
            all_sources = newsapi.get_sources(category=cat_now, country='us', language='en')
            test = all_sources['sources']
            text = ''
            for i in test:
                text += i['id'] + ','
                text = text[:len(text)-1]

        #all_str = ','.join(test)


            dat = newsapi.get_everything(q=query_now,
                                         sources= text,
                                         from_param=from_now,
                                         to=to_now,
                                         language='en',
                                         # country='us',
                                         sort_by='publishedAt',
                                         page_size=30)
        except Exception as e:
            err['message'] = str(e)
            return jsonify(e.__dict__)

        datfor = dat['articles']
        badnews = []
        for z in datfor:
            for key, value in z.items():
                if key == 'content':
                    continue

                if key == 'source':
                    x = value
                    if x['id'] is None or x['name'] is None:
                        badnews.append(z)
                        break

                if not value:
                    badnews.append(z)
                    break

        for w in badnews:
            datfor.remove(w)
        mno = datfor[:10]

        god['dat'] = mno
        print(god)

        return jsonify(god)



@application.route('/category', methods = ['GET'])
def get_sources():

    category_now = request.args.get('category')
    newsapi = NewsApiClient(api_key="34a75cc37de44563acd6cfd166285520")
    all_sources = newsapi.get_sources(category=category_now, country='us', language='en')

    return jsonify(all_sources)

@application.route('/wordcloud', methods = ['GET'])

def freq():

    words = dict()
    newsapi = NewsApiClient(api_key="34a75cc37de44563acd6cfd166285520")
    top_headlines = newsapi.get_top_headlines(q='',
                                              sources='cnn,fox-news',
                                              # domains='News.com.au',
                                              # from_param='2020-02-01',
                                              # to='2020-02-12',
                                              # category='business',
                                              language='en',
                                              # sort_by='publishedAt',
                                              page_size=30)



    res = top_headlines
    with open("stopwords_en.txt", "r") as f:
        stop_words = f.read().splitlines()
    # print(type(stop))
    stop_words.append("|")
    stop_words.append("-")
    stop_words.append("@")
    stop_words.append("_")
    stop_words.append(":")
    stop_words.append(",")
    stop_words.append(".")
    stop_words.append(";")
    stop_words.append("!")

    # print(stop_words)


    if "articles" in res:
        listw = res["articles"]


        for ls in listw:

            if "title" in ls:
                ab = re.sub(r'[^\w]]', ' ', ls['title'])
                str_list = ab.split()
                str_list = [word.lower() for word in str_list]
                store = [word for word in str_list if word not in stop_words]

                for item in store:
                    if item not in words:
                        words[item] = 1
                    else:
                        words[item] += 1

                a = sorted(words.items(), key=lambda x: x[1], reverse=True)
                bb = a[:30]
                dag = {}
                for i in bb:
                    dag[i[0]] = i[1]

    return jsonify(dag)













if __name__ == "__main__":
    application.run(debug=True)