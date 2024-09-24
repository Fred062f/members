# Members API

## Liste over øvelser lavet:

1. Kig på følgende diagram og opret et API, der følger disse ruter.
2. I stedet for at arbejde med "students", skal API'et håndtere "members".
3. Som udgangspunkt læses der fra en liste med dictionaries, som fungerer som datakilde.
4. Når API'et fungerer korrekt, skal data gemmes i en SQLite-database. Dataene fra listen skal indsættes i en tabel i databasen ved hjælp af `executemany`.
5. Hver "Member" skal have specifikke attributter.
6. API'et skal returnere den enkelte members offentlige GitHub-repositories som en del af JSON-schemas i f.eks. `api/members`-ruten. Dette kræver muligvis ændringer af `github_username` for de 10 brugere til reelle brugernavne. Det burde være relativt simpelt at håndtere dette én ad gangen via `PUT api/members`.
8. Sørg for, at de korrekte HTTP-statuskoder returneres med HTTP-responsen.
9. Husk, at der er regler for, hvad der skal ske i et GIT POST, PUT, PATCH og DELETE request. Det er helt i orden at spørge chatten om disse regler, men sørg for at skrive koden selv!
10. Sørg for at fange eventuelle fejl, som f.eks. forkert ID eller forkert JSON i body.

## Problemer med øvelser:

7. Hvis det member, der vises, er DIG, skal du også kunne se de private repositories: 
Det er ikke muligt at se dine egne private repositories med `https://api.github.com/users/{github_username}/repos`. Hvis jeg derimod bruger `https://api.github.com/repos/Fred062f/{repository}`, hvor jeg specifikt vælger et repository, som jeg ved er privat, og bruger det samme authentication token i begge API-kald, kan du jeg se det private repository.
