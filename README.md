# osakeportfolio
harjoitus
Tietokannat ja web-ohjelmointi

Aihe: Osakeportfolio

Sovelluksessa kirjautuneena käyttäjä voi luoda osakesalkkuja, joihin voi ostaa osakkeita, sekä seurata niiden arvon kehitystä.  Osakkeiden arvot ovat euroissa tai muunnettu euroiksi reaaliaikaisella kurssilla, jos ne ovat alun perin US dollareissa. Myös ostaessa osakkeita hinta ilmoitetaan euromääräisenä.  Muiden valuuttojen tapauksissa sovellus ei vielä anna oikeita hintatietoja.  Hinnat ja valuuttakurssi ladataan yfinancen avulla, joka hakee hinnat Yahoo Financen tarjoamasta palvelusta ilman että sovelluksen käyttäjä tarvitsee API-avaimia.  Hintatiedot voi esiladata käynnistyksen yhteydessä jos app.py-tiedoston initialize asetetaan arvoon True, muissa tapauksissa hinnat haetaan yksitellen ja reaaliaikaisina mutta jos tietokannassa on paljon osakkeita tämä voi aiheuttaa hitautta etenkin stocks.html-välilehdelle siirryttäessä (kyseessä ei ole varsinaisesti tietokannan hitaus vaan se että jokaisesta osakkeesta lähetetään pyyntö yfinanceen erikseen). Sovellusta voi myös käyttää ilman reaaliaikaisia tai esiladattuja hintoja jos ne eivät ole saatavilla, tällöin vain salkun ja osakkeiden markkina-arvot/tuotot ovat asetettu nollaksi.  Data.sql sisältää valmiiksi joitain Yhdysvaltojen osakkeita sekä OMX Helsingin 25- listan osakkeet ja käskyt niiden lisäämiseen tietokantaan. Osaketickerin täytyy olla oikeassa muodossa, jotta hintatiedot haetaan oikein. Salkun hallinta on vielä hyvin yksinkertaista, enkä lisännyt kaikkia lajittelukriteerejä, joita olin alun perin suunnitellut. Osakkeiden poisto yksinkertaisesti poistaa osakkeen salkusta ja sen vaikutus salkun tuottoon häviää.  SQL schema voi sisältää joidenkin taulujen osalta turhia sarakkeita, joita en ehtinyt ottamaan käyttöön, mutta mieluiten pidän ne siellä jos jostain syystä innostuisin joskus laajentamaan sovellusta.

Muilta osin sovelluksessa on käyttäjätilien rekisteröinti ja kirjautuminen, navigointi, salkkujen tarkastelu sekä luonti, osakkeiden pikalisäys sekä osakkeet-sivu, jolta löytyy kaikki tietokantaan lisätyt osakkeet.  Salasanat on kryptattu, ja suojautuminen yleisimpiä kurssimateriaalissa esitettyjä haavoittuvuuksia vastaan on pyritty toteuttamaan. Ulkoasu on pidetty selkeänä ja minimalistisena pyrkien siihen että käyttö on helppoa ja olennaiset asiat selkeästi esillä.

sovelluksen testaus:
kurssimateriaalin ohjeita mukaillen,
.env tiedostoon oma SECRET_KEY sekä oma tietokanta DATABASE_URL. Requirements.txt sisältää tarvittavat riippuvuudet. Schema.sql sisältää tietokannan rakenteen. Osakkeet täytyy lisätä itse tietokantaan, joko data.sql tiedostosta tai manuaalisesti ja sitä ei voi tehdä sovelluksen sisällä (mielestäni on parempi että sovelluksen loppukäyttäjä ei voi lisätä tietokantaan osakkeita), tässä esimerkki siihen:

INSERT INTO stocks (symbol, name, price, pe_ratio, market_cap) VALUES
('AAPL', 'Apple Inc.', 175.0, 28.5, 2750000000000),
('GOOGL', 'Alphabet Inc.', 2800.0, 30.2, 1900000000000),
('AMZN', 'Amazon.com Inc.', 135.0, 85.7, 1380000000000);

Kun Symbol-sarakkeeseen laitetaan osakkeen oikea "ticker" niin sovellus hakee reaaliaikaiset hintatiedot yfinancen avulla jos nettiyhteys on toiminnassa ja sallittu.



