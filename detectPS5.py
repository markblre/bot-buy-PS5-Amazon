from selenium import webdriver
import webbrowser
import time
import pygame.mixer
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
import buyPS5Amazon
import pushsafer
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Lien de la page Amazon à surveiller
productLinkAMAZON = "https://www.amazon.fr/PlayStation-Édition-Standard-DualSense-Couleur/dp/B08H93ZRK9/ref=sr_1_1?__mk_fr_FR=ÅMÅŽÕÑ&dchild=1&keywords=ps5&qid=1608419487&sr=8-1&th=1"

#Initialisation du comptage des scans
try:
    count = pickle.load(open("count.dat", "rb"))
except:
    count = 0
else:   
    count = count

#Initialisation de l'alarme
pygame.mixer.init()
alert = pygame.mixer.Sound("alarme.mp3")

#Initialisation des notifications
pushsafer.init("") #Private key Pushsafer

#Initialisation du navigateur automatisé
try:
    browser = webdriver.Chrome(executable_path=r"./WebDriver/chromedriver")
except SessionNotCreatedException:
    sys.exit("Mauvaise version du chromedriver: Veillez à installer une version compatible avec votre navigateur du chromedriver dans le dossier 'WebDriver'")
except:
    webdriver.Chrome(executable_path=r"./WebDriver/chromedriver")
else:
    browser.get("https://google.fr")

#Chargement des cookies de connexion Amazon
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)
    

oldTextAMAZON = "Actuellement indisponible."
newTextAMAZON = ""
while True:
    print("scan " + str(count) + " fait à " + time.strftime("%H:%M:%S", time.localtime(time.time())))
    browser.get(productLinkAMAZON)
    try:
        #recherche du texte de diponibilité
        newAMAZON = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='availability']/span"))
    )
    except TimeoutException:
        #Élément indisponible
        print("Élément non trouvé")
    except:
        #erreur
        print("Erreur")
    else:
        #Élément disponible
        newTextAMAZON = newAMAZON.text
        if(newTextAMAZON == "En stock."):
            #PS5 en STOCK
            print("STOCK DE PS5 DISPONIBLE CHEZ AMAZON!!!")
            alert.play(loops=5)
            pushsafer.Client("").send_message("Une PS5 est disponible chez AMAZON!!! Tentative d'achat en cours.", "PS5 DISPONIBLE!!!", "a", "1", "", "", productLinkAMAZON, "Open Amazon", "0", "1", "120", "120", "0", "", "", "")
            buyPS5Amazon.buyPS5AMAZON(browser, productLinkAMAZON, pushsafer)
            exit()
        elif((newTextAMAZON == "Actuellement indisponible.") or (newTextAMAZON == "Voir les offres de ces vendeurs.")):
            #PS5 indisponible
            print("La PS5 est indisponible chez AMAZON.")
        elif(newTextAMAZON != oldTextAMAZON):
            #Changement inconnu
            print("Changement inconnu sur la page AMAZON de la PS5!!!")
            webbrowser.open(productLinkAMAZON)
            alert.play(loops=5)
            pushsafer.Client("").send_message("Un changement c'est produit sur la page!", "Changement", "a", "1", "", "", productLinkAMAZON, "Open Amazon", "0", "1", "120", "120", "0", "", "", "")
            exit()
        else:
            #Erreur
            print("Inconnue")
            webbrowser.open(productLinkAMAZON)
            alert.play(loops=5)
            pushsafer.Client("").send_message("Une situation inconnue c'est produite!", "Inconnue!", "a", "1", "", "", productLinkAMAZON, "Open Amazon", "0", "1", "120", "120", "0", "", "", "")
        oldTextAMAZON = newTextAMAZON

    count += 1
    pickle.dump(count, open("count.dat", "wb"))
    time.sleep(7)
