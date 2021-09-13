import csv
import random
from flask import Flask, render_template, request
import ast

app = Flask(__name__)

path_basis = "fragen_basis.csv"
path_binnen = "fragen_binnen.csv"
path_see = "fragen_see.csv"

def load_qs():
    fragen = []
    with open(path_basis, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for row in reader:
            fragen.append( { 
                "typ": "basis",
                "frage": row["frage"],
                "nummer": row["nummer"],
                "urls": ast.literal_eval(row["bild_urls"]),
                "antworten": [row["a"],row["b"],row["c"],row["d"]],
                "richtige": row["a"],
            })

    with open(path_binnen, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for row in reader:
            fragen.append( { 
                "typ": "binnen",
                "frage": row["frage"],
                "nummer": row["nummer"],
                "urls": ast.literal_eval(row["bild_urls"]),
                "antworten": [row["a"],row["b"],row["c"],row["d"]],
                "richtige": row["a"],
            })

    with open(path_see, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for row in reader:
            fragen.append( { 
                "typ": "see",
                "frage": row["frage"],
                "nummer": row["nummer"],
                "urls": ast.literal_eval(row["bild_urls"]),
                "antworten": [row["a"],row["b"],row["c"],row["d"]],
                "richtige": row["a"],
            })
    return fragen

@app.route("/answer",methods=["GET","POST"])
def answer():
    print(request.form)
    a=int(request.form["antwort"])
    q=last_q
    print("antwort",a,q)
    print(type(a))
    return render_template("antwort.html",q=q,a_idx=a)


last_q = None

@app.route("/frage",methods=["GET","POST"])
@app.route("/")
def root():
    q = random_q()
    print(q)
    global last_q
    last_q = q
    return render_template("frage.html",q=q)

def random_q():
    q = random.choice(fragen)
    random.shuffle(q["antworten"])
    q["richtige_idx"] = q["antworten"].index(q["richtige"])
    return q

if __name__ == "__main__":
    fragen = load_qs()
    print(fragen[10])
    print(fragen[300])
    app.run(host= '0.0.0.0', debug=True)