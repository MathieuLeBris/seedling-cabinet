# Hardware – Documentation matérielle

## 1. Présentation

Cette documentation décrit l'architecture matérielle du projet Smart Seedling Cabinet, les interfaces entre les différents équipements et les principes de raccordement.

Elle constitue la référence technique pour :
- Comprendre l'organisation matérielle du système.
- Documenter les caractéristiques et le fonctionnement des composants.
- Définir les interfaces de communication.
- Préparer les raccordements électriques et électroniques.
- Centraliser les choix techniques et les schémas associés.

La nomenclature et les affectations de broches sont gérées dans des fichiers CSV. Les tableaux correspondants dans ce document sont générés automatiquement par le script `scripts/generate_hardware.py`.

**Règle de gestion :** les fichiers CSV constituent les sources de données. Les tableaux générés dans ce document ne doivent pas être modifiés manuellement.

## 2. Inventaire du matériel

La nomenclature des composants est maintenue dans :

`hardware/bom/components.csv`

Elle recense les composants nécessaires au projet, leurs références commerciales, leurs quantités et leur état d'avancement.

<!-- BOM:START -->
| ID | Composant | Fabricant | Référence | Quantité | Statut |
| --- | --- | --- | --- | --- | --- |
| CTRL-01 | Carte contrôleur | Espressif | WT32-SC01 Plus |  |  |
| SEN-01 | Capteur température / humidité | Sensirion | SHT31 |  |  |
| SEN-02 | Capteur CO2 | Sensirion | SCD41 |  |  |
| SEN-03 | Sonde température | Analog Devices | DS18B20 |  |  |
| ACT-01 | Chauffage soufflant | À définir | Équipement existant |  |  |
| ACT-02 | Tapis chauffant | À définir | Équipement existant |  |  |
| PWR-01 | Alimentation basse tension | À définir | À définir |  |  |
<!-- BOM:END -->

## 3. Architecture matérielle

Le système repose sur un contrôleur embarqué chargé de l'acquisition des mesures, de la régulation et du pilotage des équipements.

L'architecture matérielle s'organise autour de quatre fonctions principales.

### 3.1. Contrôle et interface utilisateur

Le contrôleur principal assure :
- L'acquisition des données issues des capteurs.
- Le traitement des mesures.
- L'exécution des fonctions de régulation.
- Le pilotage des équipements.
- La communication avec le serveur local.
- La gestion de l'interface tactile.

Le choix définitif du contrôleur et de son écran sera documenté après validation du matériel.

### 3.2. Instrumentation

L'instrumentation doit permettre de surveiller les conditions environnementales de l'armoire.

Les grandeurs à mesurer sont notamment :
- Température ambiante.
- Humidité relative.
- Concentration en CO₂.
- Température du substrat ou des surfaces chauffantes, si nécessaire.

L'emplacement des capteurs sera défini en fonction de la configuration de l'armoire et des zones de culture.

### 3.3. Actionneurs

Les équipements pilotés par le système comprennent :
- Le chauffage soufflant.
- Le tapis chauffant.
- Les ventilateurs.
- L'éclairage.

Le contrôleur ne pilote pas directement les équipements alimentés sur le secteur. Des interfaces de puissance adaptées, isolées et correctement dimensionnées seront nécessaires entre l'électronique basse tension et les circuits électriques existants.

### 3.4. Alimentation

L'architecture d'alimentation devra distinguer :
- L'alimentation du contrôleur.
- L'alimentation des capteurs.
- Les éventuelles alimentations des interfaces de commande.
- Les circuits de puissance des équipements.

Les tensions, intensités et protections seront documentées après sélection des composants.

## 4. Interfaces de communication

Les interfaces utilisées par les composants sont recensées dans le tableau suivant.

Ce tableau est généré automatiquement à partir de `hardware/bom/components.csv`.

<!-- INTERFACES:START -->
| Composant | Interface | Fonction | Affectation des broches |
| --- | --- | --- | --- |
| Carte contrôleur | true | GPIO / I²C | Non |
| Capteur température / humidité | true | I²C | Non |
| Capteur CO2 | true | I²C | Non |
| Sonde température | true | 1-Wire | Non |
| Chauffage soufflant | true | Relais | Non |
| Tapis chauffant | true | Relais | Non |
| Alimentation basse tension | false | DC | Non |
<!-- INTERFACES:END -->

Les principales interfaces envisagées sont :

| Interface | Utilisation | Observations |
|---|---|---|
| GPIO | Entrées et sorties numériques | Lecture et commande |
| I²C | Capteurs environnementaux | Bus partagé, adresses à vérifier |
| SPI | Périphériques nécessitant un débit supérieur | Selon contrôleur et écran |
| UART | Communication série | Selon les équipements |
| 1-Wire | Sondes de température | Résistance de pull-up nécessaire |
| Wi-Fi | Communication avec le serveur local | Réseau local |

Les interfaces réellement utilisées seront précisées après validation du contrôleur et des composants.

## 5. Affectation des broches (GPIO)

Les affectations de broches sont maintenues dans :

`hardware/bom/pin_assignments.csv`

Ce fichier permet de documenter les raccordements entre les composants et le contrôleur.

Il peut contenir plusieurs lignes pour un même composant lorsque celui-ci utilise plusieurs signaux ou broches.

Le tableau ci-dessous est généré automatiquement à partir de ce fichier.

<!-- PINS:START -->
| ID composant | Composant | Signal | GPIO | Interface | Direction | Statut | Remarques |
| --- | --- | --- | --- | --- | --- | --- | --- |
<!-- PINS:END -->

### 5.1. Règles d'affectation

L'affectation des broches doit tenir compte :
- Des broches déjà utilisées par l'écran et les périphériques intégrés.
- Des fonctions réservées par le contrôleur.
- Des contraintes électriques des entrées et sorties.
- Des éventuelles limitations propres à la carte ESP32.
- Des besoins d'extension futurs.

Les affectations ne seront considérées comme validées qu'après vérification du brochage constructeur et essais matériels.

## 6. Schémas et documentation technique

Les documents techniques associés au matériel sont organisés dans les répertoires suivants :

| Répertoire | Contenu |
|---|---|
| `hardware/bom/` | Nomenclature et affectations de broches |
| `hardware/datasheets/` | Fiches techniques constructeurs |
| `hardware/schematics/` | Schémas électroniques |
| `hardware/wiring/` | Plans de câblage et raccordements |
| `hardware/pcb/` | Fichiers de conception des circuits imprimés |

Chaque composant retenu devra, dans la mesure du possible, être associé à sa fiche technique constructeur.

Les schémas devront permettre d'identifier clairement :
- Les alimentations et leurs tensions.
- Les connexions entre le contrôleur et les capteurs.
- Les interfaces de commande des actionneurs.
- Les protections et dispositifs d'isolation.
- Les borniers et connecteurs utilisés.

## 7. Sécurité électrique

Les circuits basse tension de commande et les circuits de puissance doivent être clairement séparés.

Les interfaces de commande devront être adaptées aux caractéristiques électriques des équipements pilotés.

Les principes suivants devront être respectés :
- Isolation électrique entre la logique de commande et les circuits secteur.
- Dimensionnement adapté des relais, contacteurs ou SSR.
- Protection contre les surintensités.
- Prévention des échauffements et des courts-circuits.
- Maintien d'un fonctionnement sûr en cas de perte de communication ou de défaillance du contrôleur.

Toute intervention sur les circuits secteur doit respecter les règles de sécurité électrique applicables.

## 8. Processus de mise à jour documentaire

La documentation matérielle est alimentée par deux fichiers CSV :

| Fichier | Rôle |
|---|---|
| `hardware/bom/components.csv` | Inventaire des composants et définition des besoins d'affectation |
| `hardware/bom/pin_assignments.csv` | Affectations des signaux et broches du contrôleur |

Le script `scripts/generate_hardware.py` assure la synchronisation et la génération des tableaux.

### Procédure de mise à jour

1. Ajouter ou modifier les composants dans `components.csv`.
2. Indiquer si une affectation de broches est nécessaire.
3. Exécuter le script de génération.
4. Vérifier les nouvelles lignes créées dans `pin_assignments.csv`.
5. Compléter les signaux et les affectations GPIO.
6. Relancer le script pour actualiser les tableaux de ce document.

Commande à exécuter depuis la racine du projet :

```powershell
python scripts/generate_hardware.py
```

Les affectations déjà renseignées ne doivent pas être écrasées lors de la synchronisation.

## 9. Points à définir

- [ ] Valider le contrôleur et l'écran tactile.
- [ ] Finaliser la nomenclature des composants.
- [ ] Déterminer le nombre et l'emplacement des capteurs.
- [ ] Définir l'architecture d'alimentation basse tension.
- [ ] Définir les interfaces de commande des équipements.
- [ ] Établir l'affectation définitive des GPIO.
- [ ] Réaliser les schémas électroniques.
- [ ] Réaliser les plans de câblage.
- [ ] Valider l'intégration matérielle complète.

