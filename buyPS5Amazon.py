import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

retry = True

def addToCart(browser, productLink, pushsafer):
    #addToCart button
    try:
        addToCartButton = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        )
    except TimeoutException:
        print("add-to-cart-button non trouvé")
        if(retry):
            retry = False
            print("Nouvelle tentative...")
            browser.get(productLink)
            buyPS5AMAZON(browser, productLink, pushsafer)
    except:
        print("Erreur add-to-cart-button")
    else:
        addToCartButton.click()
        #Refus de l'assurance Amazon
        try:
            noAssurButton = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "siNoCoverage-announce"))
            )
        except TimeoutException:
            print("noAssurButton non trouvé")
        except:
            print("Erreur siNoCoverage-announce")
        else:
            time.sleep(0.5)
            noAssurButton.click()

    #buyCart button
    try:
        buyCartButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "hlb-ptc-btn-native"))
        )
    except TimeoutException:
        print("buyCartButton non trouvé")
    except:
        print("Erreur buyCartButton")
    else:
        buyCartButton.click()


def buyPS5AMAZON(browser, productLink, pushsafer):

    #buyNow button
    try:
        buyNowButton = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.ID, "buy-now-button"))
        )
    except TimeoutException:
        print("buy-now-button non trouvé")
        #ajout au panier
        addToCart(browser, productLink, pushsafer)
    except:
        print("Erreur buy-now-button")
    else:
        buyNowButton.click()
        #Refus de l'assurance
        try:
            noAssurButton = WebDriverWait(browser, 7).until(
                EC.element_to_be_clickable((By.ID, "siNoCoverage-announce"))
            )
        except TimeoutException:
            print("noAssurButton non trouvé")
        except:
            print("Erreur siNoCoverage-announce")
        else:
            time.sleep(0.5)
            noAssurButton.click()

    #login
    try:
        passwordInput = WebDriverWait(browser, 7).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
    except TimeoutException:
        print("passwordInput non trouvé")
    except:
        print("Erreur login")
    else:
        passwordInput.send_keys("") #insérer mdp Amazon
        passwordInput = browser.find_element(By.ID, "signInSubmit")
        passwordInput.click()
    
    #!! buy button !!
    try:
        buyButton = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.ID, "submitOrderButtonId"))
        )
    except TimeoutException:
        print("buyButton non trouvé")
    except:
        print("Erreur buy")
    else:
        buyButton.click()
        pushsafer.Client("").send_message("Le robot a réussi à acheter la PS5!!! Vérifiez vos commandes AMAZON!", "ACHAT EFFECTUÉ", "a", "1", "", "", productLink, "Open Amazon", "0", "1", "120", "120", "0", "", "", "")
        exit()
    
    pushsafer.Client("").send_message("Une erreur s'est produite lors de l'achat de la PS5...", "Erreur lors de l'achat!", "a", "1", "", "", productLink, "Open Amazon", "0", "1", "120", "120", "0", "", "", "")
    exit()
