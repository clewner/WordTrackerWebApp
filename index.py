from flask import Flask, render_template, redirect, url_for, request

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import jinja2

from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        
        
        
        bookname = request.form.get("bookname")
        bookname = bookname.replace(" ", "+")

        if bookname == "":
            bookname = "The+Scarlet+Letter"

        bookListUrl = "https://www.gutenberg.org/ebooks/search/?query=" + bookname.lower() + "&submit_search=Go%21"
        bookListPage = requests.get(bookListUrl)
        soupListPage = BeautifulSoup(bookListPage.content, "html.parser")
        if(soupListPage.find(class_="booklink")):
            bookTypeUrl = "https://www.gutenberg.org" + soupListPage.find(class_="booklink").find('a')['href']
            bookTypePage = requests.get(bookTypeUrl)
            soupTypePage = BeautifulSoup(bookTypePage.content, "html.parser")

            URL = "https://www.gutenberg.org" + soupTypePage.find('a', string='Read online (web)')['href']
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")


            wordlist = request.form.get("wordlist").lower()
            if wordlist == "":
                wordlist = "song-music-piano"
            wordlistlist = wordlist.split('-')

            

            results = soup.findAll("p")

            paragraphlist = []

            for x in results:
                countstring = 0
                for j in wordlistlist:
                    if re.search(r"\b" + j + r"\b", x.text):
                        countstring += 1
                
                if(countstring > 0):
                    tempstring = ""
                    if(x.find_previous_sibling(["h2", "h3"])):
                        tempstring = x.find_previous_sibling(["h2", "h3", "h4"]).text
                    else:
                        tempstring = "None"
                    
                    

                    actualtext = x.text
                    pattern = r'\[\d+\]'

                    actualtext = re.sub(pattern, '', actualtext)
                    tempstring = tempstring + "<br>" + actualtext

                    paragraphlist.append(tempstring)
            
            for y in range(len(paragraphlist)):
                for q in wordlistlist:
                    paragraphlist[y] = re.sub(r"\b" + q + r"\b", "<span style='background-color:#FFFF00'>" + q + "</span>", paragraphlist[y])

        

            return render_template('home.html', enteredbook = bookname.replace("+", " "), enteredwords = wordlist, paragraphs = paragraphlist)
        else:
            error = ["Couldn't find book"]
            return render_template('home.html', enteredbook = request.form.get("bookname"), enteredwords = request.form.get("wordlist"), paragraphs = error)
        

    else:
        return render_template('home.html', enteredbook = "", enteredwords = "", paragraphs = "")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')