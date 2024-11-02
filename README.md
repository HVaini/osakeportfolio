# osakeportfolio
harjoitus
Tietokannat ja web-ohjelmointi

Aihe: Osakeportfolio

Ideana olisi luoda sovellus jossa käyttäjä voi koostaa oman osakeportfolion osakkeista. Käyttäjätunnuksen avulla voi kirjautua omaan
"salkkuunsa" ja luoda myös uusia salkkuja. Osakkeita voi myös etsiä ja luokitella erilaisten tunnuslukujen perusteella ja myöskin
luodulle portfoliolle lasketaan erilaisia tunnuslukuja. 

Osakkeet pitänee lisätä käyttäjän/ylläpitäjän toimesta jonka jälkeen niitä voi käyttää omassa salkussaan. Voin myös ladata esimerkiksi omx 25-osakkeiden kurssit sekä keskeisimmät tunnusluvut
sovellukseen valmiiksi jonka jälkeen käyttäjä voi luoda niistä salkkunsa ja sovellus laskee ne tunnusluvut jotka on mahdollista laskea ilman aikasarjoja.

Pääpiirteissään sovelluksen kehikko olisi 
- kirjautumissivu 
- luo salkku / tarkastele salkku(j)a
   - salkun ominaisuudet
   - lisää/poista
   - arvon kehitys jos sovellukseen lisätään uusia hintanoteerauksia
- etsi osakkeita 
  - lajittele osakkeet erilaisin kriteereiin
  - lisää osakkeita salkuun

Osakkeiden/käyttäjän tiedot sekä myöskin salkun osakkeet ovat kaikki omissa SQL-taulukoissaan, luvut jotka voidaan laskea johtamalla tietokantaan tallennetuista luvuista lasketaan sovelluksen sisällä Pythonin avulla.

Aihe on pääosin sama kuin mitä ehdotin 3.periodin kurssilla viime keväänä, silloin törmäsin heti alussa ongelmiin postgreSQL:n ja windows-koneeni Ubuntun välillä ja en ehtinyt ratkaisemaan niitä ajoissa (jotka nyt selvitin jo valmiiksi). Jos aihe täytyy vaihtaa niin, saman suunnitelman mukaan voin tehdä esim. urheilusuoritusten analysointisovelluksen.
