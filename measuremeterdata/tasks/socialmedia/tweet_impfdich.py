# import packages
import PyPDF2
import re
import requests
import PIL.Image
import fitz
from io import BytesIO
import random
from pdf2image import convert_from_bytes
import tweepy
from django.conf import settings

# open the pdf file

def random_text():
    texts = [
        "Schütze dich und lass dich impfen! 🥰",
        "Los, impf dich endlich! 😡😡😡",
        "Heute ist ein guter Tag um sich impfen zu lassen! 🧐"
        "Verhindere das Schlimmste, lass dich impfen! 🤗",
        "Danke wenn auch du dich impfen lässt! 😚",
        "Ich sag nur: 💉💉💉",
        "1, 2, 3, zackzack, ab ins Impfzentrum! 🗣️",
        "Mach fürschi und la di impfä, gopf! 😤",
        "S'wär schono guet wennd'Sie sich impfä lönd, märsi! 🤨",
        "Protect yourself, get vaccinated! 🥰",
        "Заштитите се, вакцинишите се! 🥰",
        "Mbroni veten, vaksinohuni! 🥰",
        "Защитите себя, сделайте прививку! 🥰",
        "Protégez-vous, faites-vous vacciner! 🥰",
        "🥰 !از خودتون مراقبت کنید، واکسن بزنید",
        "உங்களைப் பாதுகாத்துக் கொள்ளுங்கள், தடுப்பூசி போடுங்கள்! 🥰",
        "Zaštitite se, cijepite se! 🥰",
        "Kendinizi koruyun, aşı olun! 🥰",
        "Proteggiti, fatti vaccinare! 🥰",
        "Xwe biparêzin, aşî bikin! 🥰",
        "احم نفسك ، احصل على التطعيم! 🥰",
        "خپل ځان وساتئ، واکسین وکړئ! 🥰",
        "Protektu vin, vakcinu vin! 🥰",
        "Protegia tei e lai virolar tei! 🥰",
        "💉💉 ➡ 🏋️  🦠  🚫💉 ➡ ️⚰️",
        "Vielleicht reicht es noch bevor dich @realB11529 erwischt? 😬"

    ]
    rnd_num = random.randrange(0, (len(texts)-1))

    footer = "Termin machen/Prendre rendez-vous/Prendi un appuntamento:\nhttps://bag-coronavirus.ch/impfung/impfung-planen/#cantons"
    return texts[rnd_num] + '\n\n' + footer



def generate_image():
    url = f"https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/gesundheit/corona/hauptseite/gd_zh_corona_lagebulletin.pdf"

    with requests.Session() as s:
        download = s.get(url)
        pdf_file = BytesIO(download.content)
        object = PyPDF2.PdfFileReader(pdf_file)

        # get number of pages
        NumPages = object.getNumPages()

        # define keyterms
        String = "Impfstatus der IPS-Patienten mit Covid über die Zeit"

        print(f"Search for {String}")
        # extract text and do the search
        for i in range(0, NumPages):
            PageObj = object.getPage(i)
            print("this is page " + str(i))
            Text = PageObj.extractText()
            # print(Text)
            if re.search(String, Text):
                images = convert_from_bytes(download.content)

                images[i].save('/tmp/out_image_impf.jpg', 'JPEG')


def tweet(mode):
    tweet_text = random_text()
    print(tweet_text)

    generate_image()


    #Twitter

    auth = tweepy.OAuthHandler(settings.TWITTER_IMPF_API_KEY, settings.TWITTER_IMPF_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_IMPF_ACCESS_TOKEN, settings.TWITTER_IMPF_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    if mode == "GDZ":
        media = api.media_upload("/tmp/out_image_impf.jpg")
    else:
        media = api.media_upload("/tmp/out_image_vacc.jpg")

    api.update_status(
       status=f"{tweet_text}",
       media_ids=[media.media_id_string])
