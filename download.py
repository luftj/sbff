import requests
from bs4 import BeautifulSoup

link_basis = "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-See/Basisfragen/Basisfragen-node.html"
link_see = "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-See/Spezifische-Fragen-See/Spezifische-Fragen-See-node.html"
link_binnen = "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-Binnen/Spezifische-Fragen-Binnen/Spezifische-Fragen-Binnen-node.html"

def download_fragen_basis(outfile, link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    with open(outfile, "w", encoding="utf-8") as fw:
        fw.write("nummer,frage,a,b,c,d,bild_urls\n")
        for question_block in soup.find_all("ol",type="1"):
            q = list(question_block.li.children)[0]
            # print(question_block)
            no = question_block.get("start")
            print(no)
            # print(q)
            imgs = question_block.find_all("img")
            # imgs = [i.get("src").split(".gif")[0]+".gif" for i in imgs]
            imgs = [i.get("src") for i in imgs]
            if len(imgs)>0:
                imgs_string = "[\""+"\",\"".join(imgs)+"\"]"
            else:
                imgs_string = "[]"
            # print(imgs)
            answers = question_block.ol.find_all("li")
            answer_strings = []
            for a in answers:
                a = a.text.strip()
                # print(a,"\n")
                answer_strings.append(a)
            stringstring = "','".join(answer_strings)
            fw.write("%s,'%s','%s','%s'\n" % (no,q, stringstring,imgs_string))

def download_fragen(outfile, link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    with open(outfile, "w", encoding="utf-8") as fw:
        fw.write("nummer,frage,a,b,c,d,bild_urls\n")
        for question_para in soup.find("div",id="main").find_all("p",class_=False):
            q = question_para.text.strip().replace("\n","")
            # print(question_para)
            no = q.split(". ")[0]
            q = q.replace(no+". ","")
            print(no)
            try:
                answers = question_para.find_next_sibling("ol").find_all("li")
                imgs = question_para.find_all("img")
                # imgs = [i.get("src").split(".gif")[0]+".gif" for i in imgs]
                imgs = [i.get("src") for i in imgs]
                if len(imgs)>0:
                    imgs_string = "[\""+"\",\"".join(imgs)+"\"]"
                else:
                    imgs_string = "[]"
                # print(imgs)
                answer_strings = []
                for a in answers:
                    a = a.text.strip().replace("\n","")
                    answer_strings.append(a)
                stringstring = "','".join(answer_strings)
                fw.write("%s,'%s','%s','%s'\n" % (no,q, stringstring,imgs_string))
            except:
                pass

download_fragen_basis("fragen_basis.csv", link_basis)
download_fragen("fragen_see.csv", link_see)
download_fragen("fragen_binnen.csv", link_binnen)