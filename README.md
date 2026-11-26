#  Seedling Cabinet

**Open-source smart seedling cabinet controller | ESP32, environmental monitoring, automation and local web supervision.**

## Présentation du projet

Seedling Cabinet est un projet open source visant à concevoir un système intelligent de surveillance et de pilotage d'une armoire à semis.

L'objectif est de maîtriser les conditions environnementales nécessaires au développement des semis grâce à un système d'instrumentation, d'automatisation et de supervision.

Le projet s'appuie sur un microcontrôleur ESP32 pour assurer l'acquisition des mesures, le traitement des données et le pilotage des équipements. Une interface tactile permet une utilisation locale, tandis qu'une interface Web hébergée sur un serveur local assure la supervision et le pilotage à distance.

Le développement est réalisé publiquement afin de partager les choix techniques, les réalisations, les difficultés rencontrées et les évolutions du projet.

## Fonctionnalités envisagées

- **Instrumentation :** mesure de la température, de l'humidité relative et de la concentration en CO₂.
- **Régulation thermique :** pilotage du chauffage soufflant et du tapis chauffant.
- **Ventilation :** gestion des ventilateurs et renouvellement de l'air.
- **Éclairage :** gestion et programmation des cycles lumineux.
- **Interface locale :** écran tactile pour consulter les mesures et piloter les équipements.
- **Supervision distante :** interface Web accessible depuis le réseau local.
- **Historisation :** enregistrement et consultation des données environnementales.
- **Alarmes :** surveillance des seuils et détection des anomalies de fonctionnement.

## Architecture technique

Le système s'articule autour de trois ensembles :

**1. Contrôleur embarqué**

Un microcontrôleur ESP32 assure l'acquisition des mesures, le traitement des données, les fonctions de régulation et le pilotage des équipements. Il intègre également l'interface tactile locale.

**2. Serveur local**

Un serveur héberge les services de communication, l'historisation des mesures et les fonctionnalités nécessaires à la supervision.

**3. Interface Web**

Une interface accessible depuis le réseau local permet de consulter les données, suivre leur évolution et gérer les consignes de fonctionnement.

Le contrôleur embarqué doit conserver son autonomie de fonctionnement, indépendamment de la disponibilité du serveur ou du réseau.

## Matériel et électronique

Le développement matériel repose initialement sur des modules électroniques standards afin de faciliter les essais, la validation des capteurs et la mise au point du système.

Une carte électronique d'interface personnalisée pourra être envisagée dans un second temps pour centraliser les raccordements, les alimentations et les interfaces de commande.

La documentation matérielle regroupera :
- La nomenclature des composants (BOM).
- Les fiches techniques des équipements (datasheets).
- Les schémas électroniques.
- Les plans de câblage et de raccordement.
- Les éventuels fichiers de conception PCB.

## Logiciel

Le développement logiciel comprend deux parties principales :

- **Firmware ESP32 :** acquisition des capteurs, traitement des mesures, régulation, gestion des actionneurs et interface tactile.
- **Supervision :** communication avec le contrôleur, historisation des données et interface Web.

L'architecture logicielle sera développée de manière modulaire afin de faciliter les évolutions et l'ajout de nouvelles fonctionnalités.

## Sources et projets de référence

Ce projet s'appuie sur des ressources techniques et des réalisations open source existantes.

Le projet [THL Controller – Matt Doran](https://github.com/MattDoran109/thl-controller) constitue notamment une référence pour l'architecture du contrôleur ESP32, la gestion de l'écran tactile et les fonctions de pilotage.

Les projets, bibliothèques et composants tiers utilisés seront identifiés et référencés dans la documentation, dans le respect de leurs licences respectives.

Les adaptations et développements spécifiques à Smart Seedling Cabinet seront distingués des travaux d'origine.

## Avancement du projet

Le développement est organisé en plusieurs étapes :

- [x] Construction de l'armoire à semis.
- [x] Réalisation de l'installation électrique.
- [ ] Définition de l'architecture matérielle et logicielle.
- [ ] Conception de l'instrumentation et choix des capteurs.
- [ ] Intégration et validation des mesures.
- [ ] Développement du firmware ESP32.
- [ ] Développement de l'interface tactile.
- [ ] Intégration au serveur local.
- [ ] Développement de l'interface Web.
- [ ] Essais, validation et documentation finale.

## Documentation

La documentation technique est organisée pour faciliter le développement et permettre de retrouver rapidement les informations nécessaires :

- `docs/` : architecture, fonctionnement et documentation technique.
- `hardware/` : composants, datasheets, schémas et plans de câblage.
- `firmware/` : logiciel embarqué ESP32.
- `server/` : services de communication et supervision.
- `media/` : photographies et illustrations du projet.

## Participer au projet

Ce projet est développé publiquement dans une démarche de partage et de transparence.

Les retours d'expérience, suggestions d'amélioration et contributions techniques sont les bienvenus.

L'ambition est de proposer une solution documentée, reproductible et évolutive, pouvant servir de base à la réalisation d'autres armoires à semis automatisées.

## Licence

Les conditions de réutilisation du projet et les licences des composants logiciels et matériels tiers seront précisées dans les fichiers de licence et la documentation associée.
