# Guide de Contribution

Merci de votre intérêt pour contribuer au projet "Building Professional Dashboards with Python and Tkinter" ! Ce guide vous aidera à comprendre comment contribuer efficacement.

## 🎯 Types de Contributions

Nous accueillons différents types de contributions :

### 📝 Amélioration du Contenu
- **Correction d'erreurs** dans le code ou la documentation
- **Amélioration des exemples** de code
- **Ajout d'exercices** supplémentaires
- **Clarification** des explications
- **Traduction** en d'autres langues

### 🚀 Nouvelles Fonctionnalités
- **Nouveaux widgets** personnalisés
- **Exemples supplémentaires** pour les chapitres
- **Améliorations** du dashboard final
- **Nouvelles visualisations** de données

### 🐛 Correction de Bugs
- **Problèmes de compatibilité** entre plateformes
- **Erreurs dans le code** d'exemple
- **Problèmes de performance**
- **Bugs d'interface utilisateur**

## 🔧 Comment Contribuer

### 1. Préparation de l'Environnement

1. **Fork** le repository
2. **Clone** votre fork localement :
   ```bash
   git clone https://github.com/votre-username/building-professional-dashboards.git
   cd building-professional-dashboards
   ```

3. **Installez** les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. **Créez** une branche pour votre contribution :
   ```bash
   git checkout -b feature/nom-de-votre-contribution
   ```

### 2. Standards de Code

#### Python
- **PEP 8** : Suivez les conventions de style Python
- **Docstrings** : Documentez toutes les fonctions et classes
- **Type hints** : Utilisez les annotations de type quand c'est approprié
- **Tests** : Ajoutez des tests pour les nouvelles fonctionnalités

#### Exemple de code Python :
```python
def calculate_metrics(data: List[float]) -> Dict[str, float]:
    """
    Calcule les métriques statistiques pour une liste de données.
    
    Args:
        data: Liste des valeurs numériques
        
    Returns:
        Dictionnaire contenant les métriques calculées
    """
    if not data:
        return {}
    
    return {
        'mean': sum(data) / len(data),
        'min': min(data),
        'max': max(data)
    }
```

#### Documentation
- **Markdown** : Utilisez le format Markdown pour la documentation
- **Clarté** : Écrivez de manière claire et concise
- **Exemples** : Incluez des exemples pratiques
- **Images** : Ajoutez des captures d'écran si nécessaire

### 3. Structure des Commits

Utilisez des messages de commit clairs et descriptifs :

```bash
# Bon
git commit -m "feat: ajouter widget de graphique en temps réel"

# Éviter
git commit -m "fix stuff"
```

**Préfixes recommandés :**
- `feat:` - Nouvelle fonctionnalité
- `fix:` - Correction de bug
- `docs:` - Documentation
- `style:` - Formatage du code
- `refactor:` - Refactorisation
- `test:` - Tests
- `chore:` - Maintenance

### 4. Tests

Avant de soumettre votre contribution :

1. **Testez** votre code :
   ```bash
   # Testez les exemples
   python chapters/chapter01-getting-started/hello_dashboard.py
   python chapters/chapter10-complete-professional-dashboard/main.py
   ```

2. **Vérifiez** que la documentation est à jour

3. **Assurez-vous** que le code fonctionne sur différentes plateformes

## 📋 Processus de Soumission

### 1. Pull Request

1. **Poussez** vos changements :
   ```bash
   git push origin feature/nom-de-votre-contribution
   ```

2. **Créez** une Pull Request sur GitHub

3. **Remplissez** le template de Pull Request :
   - Description claire des changements
   - Référence aux issues concernées
   - Captures d'écran si applicable

### 2. Template de Pull Request

```markdown
## Description
Brève description des changements apportés.

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Amélioration de la documentation
- [ ] Refactorisation

## Tests
- [ ] J'ai testé le code sur ma machine
- [ ] J'ai ajouté des tests si nécessaire
- [ ] Tous les tests passent

## Checklist
- [ ] Mon code suit les standards de style
- [ ] J'ai mis à jour la documentation
- [ ] J'ai ajouté des commentaires si nécessaire
- [ ] Mes changements ne cassent pas les fonctionnalités existantes
```

## 🏷️ Issues

### Signaler un Bug

Utilisez le template d'issue pour les bugs :

```markdown
## Description du Bug
Description claire et concise du bug.

## Étapes pour Reproduire
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

## Comportement Attendu
Description de ce qui devrait se passer.

## Informations Système
- OS: [ex: Windows 10, macOS, Linux]
- Python: [ex: 3.8, 3.9, 3.10]
- Version: [ex: 1.0.0]

## Captures d'Écran
Si applicable, ajoutez des captures d'écran.
```

### Demander une Fonctionnalité

```markdown
## Description
Description claire de la fonctionnalité souhaitée.

## Motivation
Pourquoi cette fonctionnalité est-elle nécessaire ?

## Solutions Alternatives
Avez-vous considéré d'autres solutions ?

## Contexte Additionnel
Toute autre information pertinente.
```

## 📞 Support

Si vous avez des questions :

1. **Consultez** la documentation existante
2. **Cherchez** dans les issues existantes
3. **Créez** une nouvelle issue si nécessaire
4. **Contactez** les mainteneurs via GitHub

## 🎉 Reconnaissance

Toutes les contributions sont appréciées ! Les contributeurs seront mentionnés dans :
- Le fichier `CONTRIBUTORS.md`
- Les remerciements du livre
- Les releases GitHub

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence MIT que le projet.

---

**Merci de contribuer à ce projet éducatif ! 🚀**
