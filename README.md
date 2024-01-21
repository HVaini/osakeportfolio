# osakeportfolio
harjoitus
Tietokannat ja web-ohjelmointi

Aihe: Osakeportfolio

Ideana olisi luoda sovellus jossa käyttäjä voi koostaa oman osakeportfolion osakkeista. Käyttäjätunnuksen avulla voi kirjautua omaan
"salkkuunsa" ja luoda myös uusia salkkuja. Osakkeita voi myös etsiä ja luokitella erilaisten tunnuslukujen perusteella ja myöskin
luodulle portfoliolle lasketaan erilaisia tunnuslukuja. 

Osakkeet pitänee lisätä käyttäjän/ylläpitäjän toimesta jonka jälkeen niitä voi käyttää omassa salkussaan. Olisi myös ehkä mahdollista 
päivittää osakkeiden kurssidata reaaliaikaisesti joka mahdollistaisi arvonmuutosten seurannan ja sellaisten tunnuslukujen laskemista joissa tarvitaan aikasarja-dataa,
mutta en tiedä onko se tarpeen aiheen laajuuden kannalta. Voin myös ladata esimerkiksi omx 25-osakkeiden kurssit sekä keskeisimmät tunnusluvut
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

Osakkeiden tiedot sekä myöskin salkun osakkeet ovat kaikki omissa SQL-taulukoissaan.
