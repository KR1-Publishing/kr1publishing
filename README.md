# kr1publishing.com

Hele nettstedet som kode. Ingen byggesteg, ingen avhengigheter.
Vercel serverer filene som de er.

```
index.html          forsiden
library.html        leveringssiden. Welcome-eposten peker hit
404.html            for gamle adresser som ikke fanges av videresending
tools/              de interaktive verktoeyene
files/              PDF-ene som lastes ned
img/                bilder
welcome-email.md    tekst og oppsett for Mailchimp-automasjonen
vercel.json         videresendinger fra gamle Wix-adresser, cache, sikkerhetshoder
robots.txt          holder biblioteket og verktoeyene ute av Google
sitemap.xml
```

**Leveringsmodellen:** ingen vedlegg i eposten. Alt ligger paa `library.html`,
og welcome-eposten inneholder én lenke dit. Da kan verktoeyene oppdateres uten
at du sender ny epost, og de interaktive verktoeyene fungerer i det hele tatt,
noe de ikke gjoer som vedlegg.

---

## Hvordan overgangen faktisk fungerer

Du beholder Wix-kontoen, domenet og eposten. Du bytter kun ut hvem som svarer
naar noen skriver kr1publishing.com i nettleseren.

Det er DNS som styrer dette:

- **A-posten og CNAME-posten** bestemmer hvilken server som leverer nettsiden.
  Disse peker du til Vercel.
- **MX-postene** bestemmer hvor eposten gaar. Disse roerer du ikke, og da
  fortsetter `contact@kr1publishing.com` noeyaktig som foer.

I det A-posten peker paa Vercel slutter Wix aa levere siden, uansett om den
staar publisert eller ikke. Du kan avpublisere Wix-siden etterpaa for ryddighets
skyld, men det er ikke noedvendig for at byttet skal virke.

**Behold disse to abonnementene:** domeneregistreringen, hvis domenet er
registrert gjennom Wix, og postkasseabonnementet, hvis eposten din ligger der.
Begge er som regel separate linjer i faktureringen, uavhengig av
Premium-planen for selve nettstedet. Finn dem under Domener og Fakturering
i Wix foer du endrer noe.

**Tips:** ta en kopi eller et skjermbilde av Wix-sidene foer du avpubliserer,
i tilfelle det ligger tekst der du vil ha tilbake.

---

## Steg 1. Legg mappen paa GitHub

1. github.com/new. Navn: `kr1publishing`. Sett den til **Private**. Ikke huk av for README.
2. Velg **uploading an existing file**.
3. Dra hele innholdet i denne mappen inn. Behold mappestrukturen.
4. Commit changes.

Mappen er allerede ryddet. Alt som ligger her skal opp.

## Steg 2. Koble til Vercel

1. vercel.com, logg inn med GitHub.
2. **Add New, Project**, velg repoet, **Import**.
3. Framework Preset: **Other**. Build Command og Output Directory staar tomme.
4. **Deploy**. Du faar en midlertidig adresse som `kr1publishing.vercel.app`.
   Aapne den og sjekk at alt ser riktig ut foer du gaar videre.

Alt fungerer paa denne adressen, ogsaa skjemaet, saa du kan teste hele
paameldingen foer domenet flyttes.

## Steg 3. Flytt domenet

I Vercel, **Settings, Domains**, legg til baade `kr1publishing.com` og
`www.kr1publishing.com`. Vercel viser hvilke poster du trenger.

I Wix, **Domener**, velg kr1publishing.com, **Avanserte innstillinger, DNS-poster**.
Endre eller legg til:

| Type  | Host  | Verdi                  |
|-------|-------|------------------------|
| A     | `@`   | `76.76.21.21`          |
| CNAME | `www` | `cname.vercel-dns.com` |

Bruk verdiene Vercel viser hvis de avviker. **La MX-postene staa som de er.**
DNS bruker fra noen minutter til et par timer. Vercel ordner HTTPS automatisk.

Naar den nye siden svarer paa domenet, kan du avpublisere Wix-siden.

**Hvis noe gaar galt:** sett A-posten tilbake til verdien Wix hadde, og den
gamle siden er tilbake innen kort tid. Derfor er det lurt aa notere den
opprinnelige verdien foer du endrer.

---

## Foer siden sendes ut til folk

Aapne `index.html` og soek etter disse tre.

**FORM-ACTION.** Mailchimp, Audience, Signup forms, Embedded form. Kopier
verdien i `action="..."` fra koden Mailchimp gir deg, og lim den inn i
`action=""` i skjemaet.

**HONEYPOT.** I samme Mailchimp-kode finnes et skjult felt som heter noe i
retning av `b_9b8e99b826134f12e16a15a13_xxxxxxx`. Bytt ut `b_XXXX_YYYY` med det
navnet. Uten dette blir paameldinger avvist som spam.

**MERGE-FELT.** I Mailchimp, Audience, Settings, Audience fields and MERGE tags,
opprett tre tekstfelt:

| Merge tag    | Brukes til                                   |
|--------------|----------------------------------------------|
| `TRACK`      | alltid `creator` fra denne siden             |
| `PICKS`      | hvilke verktoey som ble huket av             |
| `BLUEPRINT`  | `yes` hvis venteliste ble krysset av         |
| `PRICEBAND`  | prisbaandet de valgte i Blueprint-seksjonen  |

`PRICEBAND` faar en av fire verdier: `under-20`, `20-49`, `50-99`, `100-plus`.
Feltet fylles kun naar noen klikker et prisbaand, saa tomme verdier er normalt.
Det nyttige er ikke selve tallet, men fordelingen sett mot `SCORE` og `PHASE`
fra quizen. Er betalingsviljen tydelig hoeyere blant dem som allerede har gitt
ut noe, har du ikke ett produkt men en stige. Vent med aa konkludere til du har
langt over hundre svar, og husk at oppgitt betalingsvilje ligger systematisk
hoeyere enn faktisk kjoepsatferd. Tallet snevrer inn hvilket omraade du tester
ved lansering, det setter ikke prisen.

Welcome-automasjonen sender lenken til biblioteket med en gang. Teksten ligger
ferdig i `welcome-email.md`. Uten den fanger siden eposter uten aa levere noe.

---

## Videresendinger som allerede er satt opp

`vercel.json` fanger opp de gamle Wix-adressene saa ingen lenker i boekene dine
doer:

- `/product-page/...` og `/shop` gaar til DTRPG-utgiversiden med affiliate
- `/faq` gaar til spoersmaalene paa forsiden
- `/free` gaar til forsiden, siden forsiden naa er gratistilbudet
- `/general-5`, `/contact-8`, `/store-policy`, `/downloads-refunds` gaar til forsiden

Alt annet som ikke finnes lander paa `404.html`, som peker tilbake til forsiden
og til DTRPG.

## Sporingskoder ut av siden

Alle DTRPG-lenker baerer `?src=web_202608_[flate]&affiliate_id=927841`, saa du
ser i DTRPG-rapporten hvilken del av siden som sender folk videre.

## Endre noe senere

Endre filen paa GitHub, eller be Claude gjoere det. Vercel publiserer
automatisk innen et minutt etter hver commit.
