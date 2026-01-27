# Version Préliminaire - Guide Rapide

**Fichier:** `totalization_preliminary.tex`
**Objectif:** Publication arXiv rapide avec résultats n=19 (Option C)

---

## Changements par Rapport à Version Complète

### Structure Réduite
- **Pages:** ~4-6 pages (vs 8-12 prévu)
- **Sections simplifiées:** Intro → Framework → Pilot → Discussion → Future Work
- **Références:** ~20 (vs 40-60 prévu)

### Marqueurs "Preliminary"
1. **Titre:** "Preliminary Report: ..."
2. **Header rouge:** "PRELIMINARY REPORT - WORK IN PROGRESS" sur chaque page
3. **Date:** "Draft Version - Expanded Study Planned"
4. **Abstract:** Commence par note explicative
5. **Footer rouge:** Status et engagement expansion

### Honnêteté sur Limitations
- Section "Limitations" détaillée et honnête
- N=19 mentionné partout
- "Preliminary evidence" (jamais "we demonstrate")
- "Warrants expanded investigation" (pas "we prove")

### Ce Qui Est Gardé
- ✅ Framework complet (5 dimensions)
- ✅ Définition totalization
- ✅ Résultats pilot (Tableau 1)
- ✅ Mention LeCun (complémentarité)
- ✅ Plan expansion clair

### Ce Qui Est Enlevé
- ❌ Sections vides avec TODOs
- ❌ Expériences non faites (cross-model, validation humaine)
- ❌ Analyses statistiques avancées
- ❌ Appendices détaillés
- ❌ Prétentions fortes

---

## Compiler le PDF

### Option 1: Ligne de Commande

```bash
cd /home/user/anti-totalization/paper/

# Première compilation
pdflatex totalization_preliminary.tex

# Bibliographie
bibtex totalization_preliminary

# Deux compilations finales (pour références croisées)
pdflatex totalization_preliminary.tex
pdflatex totalization_preliminary.tex
```

**Résultat:** `totalization_preliminary.pdf`

### Option 2: Overleaf

1. Créez projet sur Overleaf
2. Uploadez `totalization_preliminary.tex`
3. Uploadez `references.bib`
4. Compilez (bouton "Recompile")

---

## Soumettre à arXiv

### Préparation

1. **Vérifier PDF:**
   - Headers rouges visibles
   - Toutes références correctes
   - Pas d'erreurs LaTeX

2. **Préparer fichiers:**
   ```
   totalization_preliminary.tex
   references.bib
   (figures/ si vous en ajoutez)
   ```

### Soumission arXiv

1. **Créer compte:** arxiv.org/user/register
2. **Nouvelle soumission:** "Start New Submission"
3. **Catégorie primaire:** cs.AI (Artificial Intelligence)
4. **Catégories secondaires:** cs.CY (Computers and Society), cs.LG (Machine Learning)
5. **Upload fichiers:** .tex + .bib
6. **Métadonnées:**
   - **Title:** Preliminary Report: Structural Anti-Patterns for Decision Centrality in AI Systems
   - **Authors:** [Votre nom]
   - **Abstract:** (copier depuis LaTeX)
   - **Comments:** "Preliminary report based on pilot study (n=19). Expanded validation planned. Code: https://github.com/Mesnildot/anti-totalization"

7. **Preview:** Vérifiez que PDF est correct
8. **Submit:** Soumettez!

### Après Soumission

**Délai:** ~24-48h pour modération, puis publication

**URL:** Vous recevrez `https://arxiv.org/abs/XXXX.XXXXX`

**Versions:** Vous pourrez soumettre v2, v3 plus tard avec expanded study

---

## Timeline Recommandée (Option C)

### Semaine 1 (Maintenant)
- [x] Créer version préliminaire
- [ ] Compiler PDF
- [ ] Relire + corrections typos
- [ ] Vérifier toutes références

### Semaine 2
- [ ] Feedback informel (collègues si possible)
- [ ] Ajustements mineurs
- [ ] Soumettre arXiv
- [ ] Publier sur GitHub "paper in review"

### Post-Publication
- [ ] Annoncer sur LinkedIn/Twitter
- [ ] Recueillir feedback communauté
- [ ] Planifier expanded study (Option A) si funding trouvé

---

## Différences Clés vs Version Complète

| Aspect | Preliminary (Option C) | Full (Option A) |
|--------|----------------------|-----------------|
| Pages | 4-6 | 8-12 |
| Timeline | 2 semaines | 10-15 semaines |
| Sample size | n=19 (existant) | n≥100 (nouveau) |
| Models | 1 (Gemini) | 3 (cross-validation) |
| Metrics | 1 (collapse) | 4+ (semantic, lexical, etc.) |
| Stats | Descriptif | ANOVA, effect sizes |
| Human validation | Non | Oui (n=30-50) |
| Claims | Très modestes | Robustes |
| Coût | $0 | $700-1500 |
| Qualité | "Promising direction" | "Strong evidence" |

---

## Messages Clés à Communiquer

### Lors de l'annonce (LinkedIn/Twitter):

```
Just released preliminary report on structural anti-patterns
for AI safety (totalization framework).

🔬 Pilot study (n=19) suggests structural interventions affect
decision distribution patterns.

⚠️ Early stage - expanded validation planned.

📂 Open-source: github.com/Mesnildot/anti-totalization
📄 arXiv: [lien une fois publié]

Feedback welcome!
```

### Si on vous demande "pourquoi publier preliminary?":

"To establish the conceptual framework, enable early feedback,
and transparently communicate limitations before making strong
claims. Expanded validation (n≥100, cross-model) is planned."

---

## Prochaines Étapes Après Publication

### Immédiat (1-2 semaines)
1. Surveiller feedback communauté
2. Répondre questions sur GitHub issues
3. Noter critiques constructives

### Court terme (1-3 mois)
1. Chercher funding pour expanded study
2. Identifier collaborateurs potentiels
3. Améliorer protocole basé sur feedback

### Moyen terme (3-6 mois)
1. Lancer expanded study si funding
2. Soumettre v2 avec résultats robustes
3. Considérer soumission journal/conférence

---

## Checklist Avant Soumission

- [ ] PDF compile sans erreurs
- [ ] Headers "PRELIMINARY" visibles
- [ ] Toutes limitations listées honnêtement
- [ ] Pas de claims overconfidentes
- [ ] Références complètes et correctes
- [ ] Abstract mentionne "preliminary" et "n=19"
- [ ] Future work clairement décrit
- [ ] Lien GitHub fonctionnel
- [ ] Acknowledgment AI assistance (transparent)

---

## Notes Importantes

### Ce Qui Rend Cette Approche Acceptable:

1. **Honnêteté totale** sur limitations
2. **Cadrage clair** comme preliminary
3. **Engagement explicite** à expansion
4. **Contribution conceptuelle** (framework) même si données limitées
5. **Open-source** (reproductibilité)

### Ce Qui Serait Inacceptable:

- ❌ Prétendre n=19 est suffisant
- ❌ Claims de "significance" sans stats
- ❌ Cacher que c'est preliminary
- ❌ Promettre expansion sans intention
- ❌ Garder code/données privés

---

**Vous faites les choses correctement en étant transparent sur les limites.**

C'est une approche académiquement honnête et communautaire.

---

**Dernière mise à jour:** 2026-01-27
**Fichier:** `totalization_preliminary.tex`
**Status:** Prêt pour compilation et soumission
