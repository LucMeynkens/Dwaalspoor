# Git Cheat Sheet

Een overzicht van de belangrijkste en meest gebruikte Git-commando's voor dagelijks gebruik.

## 📁 Starten & Synchroniseren
* **`git clone <link>`** – Kopieert een online repository naar je computer.
* **`git pull`** – Haalt de nieuwste wijzigingen van GitHub op en voegt ze toe aan je lokale bestanden.
* **`git status`** – Laat zien welke bestanden zijn aangepast, verwijderd of klaarstaan.

## 💾 Wijzigingen Opslaan & Pushen
* **`git add .`** – Zet **alle** gewijzigde bestanden klaar voor de volgende stap.
* **`git add <bestandsnaam>`** – Zet alleen een **specifiek** bestand klaar.
* **`git commit -m "bericht"`** – Slaat de klaargezette wijzigingen lokaal op met een beschrijving.
* **`git push origin main`** – Stuurt je lokale commits naar de online `main`-branch op GitHub.

## 🌿 Werken met Branches (Vertakkingen)
* **`git branch`** – Toont een lijst van alle lokale branches.
* **`git switch -c <branch-naam>`** – Maakt een **nieuwe** branch aan en schakelt hier direct naar over.
* **`git switch <branch-naam>`** – Schakelt over naar een **bestaande** branch.
* **`git merge <branch-naam>`** – Voegt de wijzigingen van een andere branch samen met je huidige branch.

## 🔍 Historie & Ongedaan Maken
* **`git log --oneline`** – Toont een compact overzicht van je eerdere commits.
* **`git restore <bestandsnaam>`** – Wist de wijzigingen in een bestand sinds de laatste commit.
