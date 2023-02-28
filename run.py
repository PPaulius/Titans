import os
import json
import sqlite3
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    return render_template("index.html")

# about skyrelyje naudojam informaciją iš company.json, kur aprašyti nariai.
@app.route('/about')
def about():
    data = []
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", company_data=data)

# atsidarom member puslapį kiekvieno nario atveju.
@app.route('/about/<member_name>')
def about_member(member_name):
    member = {}
    
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
                
    return render_template("member.html", member=member)

# siunčia "contact us" formos supildytus duomenis į data.db
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        conn = sqlite3.connect('data.db')
        # c = conn.cursor()
        conn.execute("INSERT INTO form_data (name, email, phone, message) VALUES (?, ?, ?, ?)", (name, email, phone, message))
        conn.commit()
        conn.close()

        flash("Thank you {}, we have received your message!".format(
            request.form["name"]))

    return render_template("contact.html", page_title="Contact")

# karjeros puslapis
@app.route('/careers')
def careers():
    return render_template("careers.html", page_title="Careers")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)