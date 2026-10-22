# Laboratorul 6 - GitHub, pas cu pas

Nume: Gutan Igor  
Grupa: SI-265  
Username GitHub: jellyfish-cyber

## Depozitele publice

- [exercitiu-git](https://github.com/jellyfish-cyber/exercitiu-git)
- [exercitiu-2](https://github.com/jellyfish-cyber/exercitiu-2)

## Pasii A1-A10

**A1.** Am folosit contul GitHub existent `jellyfish-cyber`, autentificat prin GitHub CLI.

**A2.** Am verificat instalarea Git si am exersat setarile pentru ramura `main` si `pull.rebase=false`, folosind la solicitare autorul `skipper` si adresa `your.email@example.com`.

**A3.** Am creat pe GitHub depozitul public `exercitiu-git`, cu un fisier `README.md` initial, folosind GitHub CLI.

**A4.** Am clonat depozitul pe calculator cu `git clone` si am lucrat in folderul lui, separat de depozitul disciplinei.

**A5.** Am creat si rulat `salut.py`, am verificat starea inainte si dupa `git add`, apoi am salvat schimbarea cu `git commit -m "Adaug salut.py"`.

**A6.** Am trimis commit-ul pe GitHub cu `git push` si am verificat sincronizarea ramurii locale cu `origin/main`.

**A7.** Am adaugat pe GitHub randul `Aici exersez git.` in `README.md`, prin GitHub CLI, apoi am adus commit-ul pe calculator cu `git pull`.

**A8.** Am creat mediul virtual `.venv`, l-am observat in `git status`, apoi am adaugat regulile `.venv/` si `__pycache__/` in `.gitignore`, am facut commit si push.

**A9.** Am citit cele patru commit-uri cu `git log --oneline`, am adaugat temporar `print("al doilea")` in `salut.py`, am vazut schimbarea cu `git diff` si am anulat-o cu `git restore salut.py`.

**A10.** Am initializat local `exercitiu-2` cu `git init`, am creat si comis `README.md`, apoi am creat depozitul public gol pe GitHub, am adaugat `origin` si am publicat ramura cu `git push -u origin main`.

## Asistenta si conditii de predare

Operatiile si redactarea raportului au fost realizate cu asistenta Codex, pe baza fisei `L6_Laborator_GitHub_pas_cu_pas.docx`; operatiile pe GitHub au fost efectuate prin GitHub CLI.

La solicitare, depozitul disciplinei isi pastreaza numele `Laboratoare`, iar commit-urile folosesc autorul `skipper` si adresa de e-mail placeholder `your.email@example.com`; acestea difera de denumirea si identitatea cerute in fisa.
