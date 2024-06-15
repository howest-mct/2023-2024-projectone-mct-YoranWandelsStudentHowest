# Projectgegevens

**VOORNAAM NAAM:** Yoran Wandels

**Sparringpartner:** Sarkis Mukoyan

**Projectsamenvatting in max 10 woorden:** Een proteine shake dispenser met bediening via website en hardware

**Projecttitel:** Musclefuel dispenser

# Tips voor feedbackgesprekken

## Voorbereiding

> Bepaal voor jezelf waar je graag feedback op wil. Schrijf op voorhand een aantal punten op waar je zeker feedback over wil krijgen. Op die manier zal het feedbackgesprek gerichter verlopen en zullen vragen, die je zeker beantwoord wil hebben, aan bod komen.

## Tijdens het gesprek:

> **Luister actief:** Schiet niet onmiddellijk in de verdediging maar probeer goed te luisteren. Laat verbaal en non-verbaal ook zien dat je aandacht hebt voor de feedback door een open houding (oogcontact, rechte houding), door het maken van aantekeningen, knikken...

> **Maak notities:** Schrijf de feedback op zo heb je ze nog nadien. Noteer de kernwoorden en zoek naar een snelle noteer methode voor jezelf. Als je goed noteert,kan je op het einde van het gesprek je belangrijkste feedback punten kort overlopen.

> **Vat samen:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.

> **Sta open voor de feedback:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.`

> **Denk erover na:** Denk na over wat je met de feedback gaat doen en koppel terug. Vind je de opmerkingen terecht of onterecht? Herken je je in de feedback? Op welke manier ga je dit aanpakken?

## NA HET GESPREK

> Herlees je notities en maak actiepunten. Maak keuzes uit alle feedback die je kreeg: Waar kan je mee aan de slag en wat laat je even rusten. Wat waren de prioriteiten? Neem de opdrachtfiche er nog eens bij om je focuspunten te bepalen.Noteer je actiepunten op de feedbackfiche.

# Feedforward gesprekken

## Gesprek 1 (Datum: 5/24/2024)

Lector: Tijn

Vragen voor dit gesprek:

- vraag 1:

    - Reflectie van mijn fritzing schema

- vraag 2:

    - Reflectie van mijn lasercut design

Dit is de feedback op mijn vragen.

- feedback 1:

    - geen mcp gebruiken, ik zou moeten genoeg gpio pins hebben

    - 1k ohm voor de button

    - rotary encoder op 3.3v en niet 5v

    - een ground voor de pcf

    - zorgen dat de 2 stappenmotors niet tegelijk werken

    - een weerstand op de transistor voor de waterpomp, begin met 1k ohm en als het te traag pompt veranderen met 100 ohm

- feedback 2:

    - nog tanden toevoegen aan de lasercut design deepnest gebruiken om de onderdelen zo efficient mogelijk te plaatsen


## Gesprek 2 (Datum: 5/24/2024)

Lector: Frederik

Vragen voor dit gesprek:

- vraag 1:

    - Reflectie schema database

Dit is de feedback op mijn vragen.

- feedback 1:

    - extra tabel gebruikers om te kunnen weten wie welke doseringen neemt

    - geen extra tabel voor de shakes bij te houden want heb je al in historiek


## Gesprek 3 (Datum: 5/29/2024)

Lector: Christophe

Vragen voor dit gesprek:

- vraag 1:

    - Probleem met database connectie

- vraag 2:
    - Probleem met socketio connectie

Dit is de feedback op mijn vragen.

- feedback 1:

    - lgpio opnieuw instaleren

- feedback 2:

    - ip adress gebruiken als url, socketio server starten in de backend

## MVP2 (Datum: 4/7/2024)

Lector: Stijn, Pieter-Jan, Frederik

Vragen voor dit gesprek:

 - vraag 1:

    - Raspberry pi valt vaak uit

Dit is de feedback op mijn vragen.

    - feedback 1:
        - alles was in orde

## MVP3 (Datum: 6/12/2024)

Lector: Geert, Claudia, Dieter

Dit is de feedback

    - feedback:
        - grafiek cumulatief tonen en tonen hoeveel shakes je per week gedronken hebt
        - trechter voor de poeder eruit te doen
        - realistiche kleuren voor de charts
        - logo van muscluefuel dispenser laten staan bij kleinere schermen
    
## Gesprek 4 (Datum: 6/14/2024)

Lector: Christophe

Vragen voor dit gesprek:

 - vraag 1:

    - weight sensors worden niet gecalibreerd

 - vraag 2:

    - feedback website

Dit is de feedback op mijn vragen.

    - feedback 1:

        - de calibratie file moest absoluut gelezen worden

    - feedback 2:

        - label voor de charts, tonen met wat de machine bezig is als je een shake maakt, shutdown button toevoegen, wanneer er een shake gemaakt word moet de code in een aparte thread zodat er nog andere functies kunnen gebeuren, tonen op welke pagina je zit
