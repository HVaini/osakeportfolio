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



päivitys 1.12:

Sovelluksen toiminnallisuudet ovat pääosin valmiit ja toimivat. Osakkeiden poisto (tai "poisto/piilotus") käyttäjän portfoliosta on ainut lisäys jonka aion toteuttaa mutta se on osoittautunut hieman hankalaksi ja testailen vielä paria eri vaihtoehtoa. Ulkoasu/käytettävyys on edelleen kömpelö mutta aion viimeistellä sen kun sovellus on muilta osin valmis. Tietoturvaan aion myös keskittyä, ainakin CSFR puuttuu vielä mutta muilta osin kurssimateriaalissa olevat haavoittuvuudet lienevät kunnossa (tosin tähän pitää vielä perehtyä). Lisäksi jaan vielä sovelluksen useampiin tiedostoihin funktioiden perusteella. 

sovelluksen testaus:
kurssimateriaalin ohjeita mukaillen,
.env tiedostoon oma SECRET_KEY sekä oma tietokanta DATABASE_URL. Requirements.txt sisältää tarvittavat riippuvuudet. Schema.sql sisältää tietokannan rakenteen. Osakkeet täytyy lisätä itse tietokantaan ja sitä ei voi tehdä sovelluksen sisällä, tässä esimerkki siihen:

INSERT INTO stocks (symbol, name, price, pe_ratio, market_cap) VALUES
('AAPL', 'Apple Inc.', 175.0, 28.5, 2750000000000),
('GOOGL', 'Alphabet Inc.', 2800.0, 30.2, 1900000000000),
('AMZN', 'Amazon.com Inc.', 135.0, 85.7, 1380000000000);

Kun Symbol-sarakkeeseen laitetaan osakkeen oikea "ticker" niin sovellus hakee reaaliaikaiset hintatiedot yfinancen avulla jos nettiyhteys on toiminnassa ja sallittu.



