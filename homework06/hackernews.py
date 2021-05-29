from bottle import (
    route, run, template, request, redirect
)

from bayes import NaiveBayesClassifier
from scraputils import get_news
from db import News, session


@route("/news")
def news_list():
    
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():

    lb = request.query["label"]
    id = request.query["id"]
    s = session()
    p = s.query(News).get(id1)
    p.lb = lb
    session.add(s)
    session.commit()
    redirect("/news")


@route("/update")
def update_news():

    s = session()
    lk = get_news("https://news.ycombinator.com/newest", 1)
    for i in range(len(lk)):
        n = News(
            title=pages[i]["title"],
            author=pages[i]["author"],
            comments=pages[i]["comments"],
            points=pages[i]["points"],
            url=pages[i]["url"],
        )
        if (
            s.query(News).filter(News.title == a.title and News.author == a.author).count()
            == 0
        ):
            s.add(a)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():

    s = session()
    unclassified: tp.List[tp.Tuple[int, str]] = [
        (i.id, stemmer.clear(i.title))
        for i in sess.query(News).filter(News.label == None).all()
    ]
    X = [i[1] for i in unclassified]
    if not pathlib.Path(
            f"{os.path.dirname(os.path.realpath(__file__))}/../model/model.pickle"
    ).is_file():
        raise ValueError(
            "Classifier is untrained! Please mark enough news to adequately train the model and run bayes.py to save it."
        )
    with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/../model/model.pickle", "rb"
    ) as model_file:
        model = NaiveBayesClassifier(alpha=0.1)
        model = pickle.load(model_file)
    lb = model.predict(X)
    for i, e in enumerate(unclassified):
        extract = s.query(News).filter(News.id == e[0]).first()
        extract.label = lb[i]
        s.commit()
    rows = s.query(News).filter(News.label != None).order_by(News.label).all()

    return template("classified_template.tpl", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)

