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

päivitys 17.11:

Sovelluksen perusrakenne toimii, mukaanlukien kirjautuminen, käyttäjätilien luonti, portfolioiden luonti ja osakkeiden lisäys portfolioihin. Sovellus on vielä hyvin karkean näköinen koska olen keskittynyt ainoastaan siihen että kaikki perustoiminnallisuudet ovat kunnossa ja toimivat moitteetta. Tietoturva on myöskin vielä täysin huomioimatta (lukuunottamatta SQL parametrien sanitointia). Seuraavaksi tavoitteena olisi kehittää vielä osakkeiden lajittelua, lisää tunnuslukuja osakkeille ja mahdollistaa niiden selaaminen ja valinta ilman tämänhetkistä kömpelöhköä liukuvalikkoa, sekä myöskin kehittää portfolio-tason raportointia. Tämän jälkeen aion keskittyä tietoturvaan, varmistaa että sessio päättyy aina (tällä hetkellä vaatii uloskirjautumisen jos järjestelmää ei suljeta kokonaan) sekä sovelluksen ulkoasun parantamiseen.

sovelluksen testaus:
kurssimateriaalin ohjeita mukaillen,
.env tiedostoon oma SECRET_KEY sekä oma tietokanta DATABASE_URL. Requirements.txt sisältää tarvittavat riippuvuudet. Schema.sql sisältää tietokannan rakenteen. Osakkeet täytyy lisätä itse tietokantaan ja sitä ei tällä hetkellä voi vielä tehdä sovelluksen sisällä, tässä esimerkki siihen:

INSERT INTO stocks (symbol, name, price, pe_ratio, market_cap) VALUES
('AAPL', 'Apple Inc.', 175.0, 28.5, 2750000000000),
('GOOGL', 'Alphabet Inc.', 2800.0, 30.2, 1900000000000),
('AMZN', 'Amazon.com Inc.', 135.0, 85.7, 1380000000000);



