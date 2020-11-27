# Esse bot checa as lojas mais importantes no brasil quanto a disponibilidade de PS5 versão digital
# ele cicla tentando loja após loja, se houver estoque, ele envia email pro email cadastrado na função send_email
# esse bot usa o webdriver do selenium - esse webdriver precisa estar previamente instalado e funcionando.
# o programa foi escrito usando o webdriver do chrome
# veja esse link: https://chromedriver.chromium.org/getting-started
# você precisa colocar o seu email e senha do gmail pra o bot poder funcionar.
# está configurado para o gmail
# o gmail tem senhas de aplicativos, recomenda-se que use senha de aplicativo, do contrário a autenticação em duas
# etapas vai lhe prejudicar
# sobre senhas de aplicativos do gmail: https://support.google.com/mail/answer/185833?hl=pt-BR
# recomendo que você programe dentro do arquivo .py o seu email e senha pra não ter que digitar toda vida que iniciar
# o script.
# faça bom uso! boa sorte!
# autor: Heleno Paiva - heleno@gmail.com

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import smtplib
import time

# aqui você pode colocar seu login e senha. eu recomendo que voce customize o código e pule esta estapa.
email = input("digite o seu email: ")
senha = input("digite a senha do seu email: ")

# o site do amazon é simples, dá pra resolver com o requests.
def check_amazonbr():
    try:
        url = 'https://www.amazon.com.br/dp/B08CWG5K2D'
        headers = {"User agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find(id="availability").get_text()
        # o amazon permite que terceiros vendam dentro do link deles - isso prejudica o bot: por isso criei uma
        # excessão para driblar o marketplace
        if title.strip() == "Disponível com estes vendedores.":
            print("amazon BR só com marketplace")
        elif title[4:18] == "Não disponível":
            print("amazon BR indisponível")
        else:
            print("PS5 no Amazon BR")
            send_email("PS5 no AMAZON BR!!!", "https://www.amazon.com.br/dp/B08CWG5K2D")
    except:
        print("erro na funcao do amazon BR")
        time.sleep(1)

# o Extra já é um site mais complicado e precisei usar o selenium - vai abrir uma janela e ela vai fechar sozinha
def check_extra():
    try:
        PATH = "/Users/heleno/PycharmProjects/chromedriver"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.extra.com.br/Games/playstation5/consoles-playstation5/console-playstation-5-digital-edition-controle-sem-fio-dualsense-55010439.html?IdSku=55010439")
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        available = soup.find(id="titleAvailability").get_text()
        driver.quit()
        if available == "Infelizmente não temos estoque do produto que você está procurando no momento.":
            print("extra indisponivel")
        else:
            print("PS5 no Extra!")
            send_email("PS5 no EXTRA!!!", "https://www.extra.com.br/Games/playstation5/consoles-playstation5/console-playstation-5-digital-edition-controle-sem-fio-dualsense-55010439.html?IdSku=55010439")
    except:
        print("erro na funcao do extra")
        time.sleep(1)
        driver.quit()

# o Magazine Luiza também tem um site simples que dá pra usar o requests.
def check_magalu():
    try:
        url = 'https://www.magazineluiza.com.br/console-playstation-5-digital-edition-ps5-sony/p/043079600/ga/gps5/'
        headers = {"User agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find("p").get_text()
        if title == "Não disponível":
            print("magalu indisponível")
        else:
            print("PS5 em Magazine Luiza!")
            send_email("PS5 no MAGAZINE LUIZA!!!", "https://www.magazineluiza.com.br/console-playstation-5-digital-edition-ps5-sony/p/043079600/ga/gps5/")
    except:
        print("erro na funcao do magalu")
        time.sleep(1)

# o ponto frio também requer o selenium
def check_pontofrio():
    try:
        PATH = "/Users/heleno/PycharmProjects/chromedriver"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.pontofrio.com.br/console-playstation-5-digital-edition-controle-sem-fio-dualsense/p/55010439")
        soup = BeautifulSoup(driver.page_source, "lxml")
        available = soup.find(id="titleAvailability").get_text()
        driver.quit()
        if available == "Infelizmente não temos estoque do produto que você está procurando no momento.":
            print("ponto frio indisponível")
        else:
            print("PS5 no Ponto Frio!")
            send_email("PS5 no PONTO FRIO", "https://www.pontofrio.com.br/console-playstation-5-digital-edition-controle-sem-fio-dualsense/p/55010439")
    except:
        print("erro na funcao do ponto frio")
        time.sleep(1)
        driver.quit()

# inclui o amazon US também porque as vezes vale a pena pagar os impostos e receber aqui. usando selenium:
def check_amazonus():
    try:
        PATH = "/Users/heleno/PycharmProjects/chromedriver"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.amazon.com/gp/product/B08FC6MR62?")
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        available = (soup.find(class_="a-size-medium a-color-price").get_text().strip())
        if available == "Currently unavailable.":
            print("amazon US indisponível")
        else:
            send_email("PS5 no AMAZON US", "https://www.amazon.com/gp/product/B08FC6MR62?")
    except:
        print("erro na funcao do amazon US")
        time.sleep(1)
        driver.quit()


# Essa função envia email
# tá configurada para o gmail
# vale a pena modificar as funcões server.login e server.sendmail pra já ficar com o seu email automático.
def send_email(subject, body):
    # usando smtplib
    # 587 é a porta que essa livraria usa o gmail.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, senha)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, msg)
    print("Email Enviado!!!")
    server.quit()

# esse é o core do programa: ele vai ficar em loop eterno checando os sites em questão.
# mesmo quando chegue estoque, deve demorar poucos minutos para esgotar,
# o timer de 5 segundos é um dispositivo de cordialidade do bot para que ele não dispare muito rápido contra os sites.
# se os sites em questão forem acessados muito rapidamente, o servidor pode reconhecer como bot malicioso e proibir o
# acesso do seu ip.
#while true faz que o loop seja infinito.
while True:
    time.sleep(5)
    check_amazonbr()
    check_extra()
    check_magalu()
    check_pontofrio()
    check_amazonus()
