from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from aiLib import AiClassify

classifier = AiClassify()
site = "https://www.technopolis.bg/bg//Kompyut%C3%A0rni-aksesoari/Mishki-i-klaviaturi/Klaviaturi/c/P11020202?pageselect=90&page=0"
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get(site)
#accept cookies
# btns = driver.find_elements(By.TAG_NAME, "button")
# for btn in btns:
#     text = ' '.join(btn.text.split())
#     if classifier.isCookieAccept(text):
#         print("here")
#         if (btn.parent.getText().equalsIgnoreCase("cookie")):
#             print("ok")
links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    if classifier.isCookieAccept(link)!=-1:
        link.click()
        break

res = []
while True:
    site = driver.current_url

    #auto products
    res = driver.execute_script('''
    let candidates = [...document.querySelectorAll("*")].sort((a,b)=>[...b.children].filter(c=>c.tagName!="SCRIPT").length - [...a.children].filter(c=>c.tagName!="SCRIPT").length)
  return candidates.length
    ''')
    for i in range(0, res):
        textCon = driver.execute_script('''
        function createXPathFromElement(elm) { 
        var allNodes = document.getElementsByTagName('*'); 
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
        { 
            if (elm.hasAttribute('id')) { 
                    var uniqueIdCount = 0; 
                    for (var n=0;n < allNodes.length;n++) { 
                        if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++; 
                        if (uniqueIdCount > 1) break; 
                    }; 
                    if ( uniqueIdCount == 1) { 
                        segs.unshift('id("' + elm.getAttribute('id') + '")'); 
                        return segs.join('/'); 
                    } else { 
                        segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]'); 
                    } 
            } else if (elm.hasAttribute('class')) { 
                segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]'); 
            } else { 
                for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                    if (sib.localName == elm.localName)  i++; }; 
                    segs.unshift(elm.localName.toLowerCase() + '[' + i + ']'); 
            }; 
        }; 
        return segs.length ? '/' + segs.join('/') : null; 
    }; 
        let candidates = [...document.querySelectorAll("*")].sort((a,b)=>[...b.children].filter(c=>c.tagName!="SCRIPT").length - [...a.children].filter(c=>c.tagName!="SCRIPT").length)
    function stripScripts(s) {
    var div = document.createElement('div');
    div.innerHTML = s.innerHTML;
    var scripts = div.getElementsByTagName('script');
    var i = scripts.length;
    while (i--) {
      scripts[i].parentNode.removeChild(scripts[i]);
    }
    return [div.textContent.split(), createXPathFromElement(s)];
  }
        return stripScripts(candidates[''' + str(i) +'''].children[0])''')
        res = classifier.isProduct(textCon[0][0].replace('\n', ''))
        print(res)
        if res is not None:
            print(textCon[1])
            break
    products = driver.find_elements(By.CSS_SELECTOR, ".products-grid-list .list-item .product-box")
    for product in products:
        print(product.find_element(By.CSS_SELECTOR, ".product-box__middle h3 .product-box__title-link"))
        res.append({
            "title": product.find_element(By.CSS_SELECTOR, ".product-box__middle h3 .product-box__title-link").text.replace("Клавиатура ", ""),
            "price": product.find_element(By.CSS_SELECTOR, ".product-box__bottom .product-box__bottom-top .product-box__prices .product-box__price .product-box__price-value").text
        })
    #find pagination
    import autopager
    import requests
    selector = autopager.extract(requests.get(site), next=True)
    nextPages = [s for s in selector if s[0]=="NEXT"]
    print(nextPages)
    if len(nextPages) == 0:
        break
    nextPageHtml = nextPages[0][1].extract()
    script = '''
    function createXPathFromElement(elm) { 
        var allNodes = document.getElementsByTagName('*'); 
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
        { 
            if (elm.hasAttribute('id')) { 
                    var uniqueIdCount = 0; 
                    for (var n=0;n < allNodes.length;n++) { 
                        if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++; 
                        if (uniqueIdCount > 1) break; 
                    }; 
                    if ( uniqueIdCount == 1) { 
                        segs.unshift('id("' + elm.getAttribute('id') + '")'); 
                        return segs.join('/'); 
                    } else { 
                        segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]'); 
                    } 
            } else if (elm.hasAttribute('class')) { 
                segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]'); 
            } else { 
                for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                    if (sib.localName == elm.localName)  i++; }; 
                    segs.unshift(elm.localName.toLowerCase() + '[' + i + ']'); 
            }; 
        }; 
        return segs.length ? '/' + segs.join('/') : null; 
    }; 
    return createXPathFromElement([...document.querySelectorAll("*")].filter(d=>d.outerHTML==`''' + nextPageHtml + '''`)[0])
    '''
    xpath = driver.execute_script(script)
    driver.find_element(By.XPATH, xpath).click()
    products = driver.find_elements(By.CSS_SELECTOR, ".products-grid-list .list-item .product-box")
    for product in products:
        res.append({
            "title": product.find_element(By.CSS_SELECTOR, ".product-box__middle h3 .product-box__title-link").text.replace("Клавиатура ", ""),
            "price": product.find_element(By.CSS_SELECTOR, ".product-box__bottom .product-box__bottom-top .product-box__prices .product-box__price .product-box__price-value").text
        })
    print("here")

print(res)