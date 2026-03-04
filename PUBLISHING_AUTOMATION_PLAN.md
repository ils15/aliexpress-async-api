# 🚀 PLANO ORQUESTRADO: Automação PyPI com GitHub Actions + Versioning + Changelog

## 📋 OBJETIVO
**Automatizar publicação no PyPI**: A cada merge em `master`, GitHub Actions:
1. Valida testes e cobertura
2. Gera versão automática (semântico)
3. Cria changelog estruturado
4. Faz build do pacote
5. Publica no PyPI automaticamente

---

## 🏗️ ARQUITETURA DA SOLUÇÃO

```
Developer Push → Git Master
        ↓
GitHub Actions Triggered
        ↓
├─ 1️⃣ Test & Validate (103 tests, 89% coverage)
├─ 2️⃣ Version Bumping (semântico automático)
├─ 3️⃣ Changelog Generation (structured)
├─ 4️⃣ Build Package (wheel + sdist)
└─ 5️⃣ Publish to PyPI (automatic)
        ↓
PyPI Updated
        ↓
pip install aliexpress-async-api  ✅ NOVO VERSION
```

---

## ⚙️ COMPONENTES A CRIAR

### 1️⃣ **GitHub Actions Workflow**
- Nome: `.github/workflows/publish.yml`
- Triggered: On push to master with tests passing
- Actions:
  - Run pytest (skip if failed)
  - Bump version (major.minor.patch)
  - Generate changelog
  - Build wheel + sdist
  - Publish to PyPI

### 2️⃣ **Versioning Strategy** (Semântico)
- **MAJOR** (1.0 → 2.0): Breaking changes
- **MINOR** (1.0 → 1.1): New features (Features 1-5)
- **PATCH** (1.0 → 1.0.1): Bug fixes
- Detecção automática via commit messages

### 3️⃣ **Changelog Automation**
- Parseador: Extrai features/fixes do commit message
- Formato: Markdown estruturado
- Mantém histórico completo
- Sincroniza com GitHub Releases

### 4️⃣ **PyPI Integration**
- Token de autenticação (secrets em GitHub)
- Configuração em `pyproject.toml`
- Auto-publish com `twine`

### 5️⃣ **GitHub Releases**
- Cria release automática com tag
- Inclui changelog do commit
- Linkado ao PyPI version

---

## 📝 FASES DE IMPLEMENTAÇÃO

### FASE 1: Configuração PyPI (10 min)
- [ ] Criar conta/token PyPI
- [ ] Adicionar em GitHub Secrets
- [ ] Configurar pyproject.toml com versioning dinâmico

### FASE 2: GitHub Actions Workflow (20 min)
- [ ] Criar `.github/workflows/publish.yml`
- [ ] Configurar job matrix para testes
- [ ] Integrar versioning automático
- [ ] Integrar changelog generation
- [ ] Configurar upload para PyPI

### FASE 3: Changelog & Versioning (15 min)
- [ ] Criar script Python para bump version
- [ ] Criar script para gerar changelog
- [ ] Integrar em workflow como step

### FASE 4: Testing & Validation (20 min)
- [ ] Testar workflow localmente (act)
- [ ] Testar versioning
- [ ] Testar upload para TestPyPI
- [ ] Validar GitHub Release

### FASE 5: Documentation (10 min)
- [ ] Documenter versioning strategy
- [ ] Criar PUBLISHING.md
- [ ] Adicionar badge PyPI ao README

---

## 🔑 ARTIFACTS A CRIAR

```
✅ CRIAR:
├── .github/workflows/publish.yml          (GitHub Actions workflow)
├── scripts/bump_version.py                (Semântico versioning)
├── scripts/generate_changelog.py          (Changelog automático)
├── PUBLISHING.md                          (Documentação)
└── .github/configs/pypi-config.toml       (PyPI settings)

✅ ATUALIZAR:
├── pyproject.toml                         (Dynamic versioning)
├── README.md                              (PyPI badge)
└── .gitignore                             (dist/, build/)
```

---

## 🛠️ WORKFLOW AUTOMÁTICO

### Quando: Push em `master` com `[release]` ou semântica detectada

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    branches:
      - master
    paths:
      - 'aliexpress_async_api/**'
      - 'tests/**'

jobs:
  test-and-publish:
    runs-on: ubuntu-latest
    
    steps:
      # 1️⃣ Test
      - run: pytest tests/ --cov --cov-report=xml
      
      # 2️⃣ Bump Version (via commit message)
      - run: python scripts/bump_version.py
        env:
          GIT_COMMIT: ${{ github.event.head_commit.message }}
      
      # 3️⃣ Generate Changelog
      - run: python scripts/generate_changelog.py
      
      # 4️⃣ Build
      - run: |
          python -m pip install build
          python -m build
      
      # 5️⃣ Publish to PyPI
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
      
      # 6️⃣ Create GitHub Release
      - run: gh release create v$VERSION --notes-file CHANGELOG.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📊 VERSIONING AUTOMÁTICO

### Detecção via Commit Message:

```
feat(...): Add new feature       → MINOR (1.0 → 1.1)
fix(...): Bug fix                → PATCH (1.0 → 1.0.1)
feat(feat): Breaking change      → MAJOR (1.0 → 2.0)
docs(...): Documentation         → NÃO PUBLICA
test(...): Test changes          → NÃO PUBLICA
refactor(...): Code quality      → PATCH (1.0 → 1.0.1)
```

### Exemplo v1.0.0 → v1.1.0 (próxima feature):
```bash
git commit -m "feat(feature6): Add XYZ support"
# ↓
# GitHub Actions detecta "feat"
# ↓
# Bumpa de 1.0.0 → 1.1.0
# ↓
# Publica em PyPI automaticamente
```

---

## 📝 CHANGELOG AUTOMÁTICO

### Formato Estruturado:

```markdown
## [1.1.0] - 2026-03-05

### Added
- Feature 6: XYZ support (via commit)
- New endpoint for ABC

### Changed
- Improved error handling
- Optimized rate limiter

### Fixed
- Bug in webhook dispatch

### Security
- Updated dependencies
```

**Gerado automáticamente a partir dos commits!**

---

## 🔐 CONFIGURAÇÃO PyPI

### 1️⃣ Criar Token PyPI

Na conta PyPI:
```
Settings → API Tokens → Create token
Scope: Project (aliexpress-async-api)
Copiar token (única vez)
```

### 2️⃣ Adicionar ao GitHub Secrets

```
Repository Settings → Secrets → New secret
Name: PYPI_API_TOKEN
Value: pypa-XXXXXXXXXXXX
```

### 3️⃣ Configurar pyproject.toml

```toml
[project]
name = "aliexpress-async-api"
dynamic = ["version"]  # ← Dinâmica (não hardcoded)
```

---

## 🚀 FLUXO COMPLETO

### Cenário: Nova Feature
```
1. Dev faz feature (ex: Feature 6)
2. Testa localmente (pytest)
3. Faz commit com: "feat(feature6): Add support"
4. git push origin master
   ↓
5. GitHub Actions triggered:
   - Roda 103 testes ✅
   - Detecta "feat" → MINOR bump
   - 1.0.0 → 1.1.0
   - Gera changelog
   - Build wheel + sdist
   - Upload para PyPI
   - Cria GitHub Release v1.1.0
   ↓
6. pip install aliexpress-async-api==1.1.0 ✅
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Ordem de Execução:

- [ ] **PASSO 1**: Criar scripts de versioning e changelog (15 min)
  - Criar `scripts/bump_version.py`
  - Criar `scripts/generate_changelog.py`

- [ ] **PASSO 2**: Atualizar pyproject.toml (5 min)
  - Adicionar `dynamic = ["version"]`
  - Configurar build backend

- [ ] **PASSO 3**: Criar GitHub Actions workflow (10 min)
  - Criar `.github/workflows/publish.yml`
  - Adicionar testes, versioning, build, publish steps

- [ ] **PASSO 4**: Configurar PyPI Token (5 min)
  - Criar token no PyPI
  - Adicionar ao GitHub Secrets

- [ ] **PASSO 5**: Documentação (10 min)
  - Criar PUBLISHING.md
  - Atualizar README com badge

- [ ] **PASSO 6**: Testar (20 min)
  - Testar com TestPyPI
  - Simular workflow localmente

---

## 🎯 RESULTADO FINAL

**Após implementação:**

```
✅ Automação Completa
   ├─ Push → GitHub → Tests → Version → Build → PyPI
   ├─ Changelog automático
   ├─ GitHub Releases sincronizadas
   └─ Zero manual steps

✅ Histórico Estruturado
   ├─ Cada commit = feature/fix/refactor rastreável
   ├─ Changelog gerado automaticamente
   └─ Versioning semântico automático

✅ Pronto para Produção
   ├─ PyPI com versioning automático
   ├─ Instalável via pip
   └─ Histórico de releases
```

---

## 📚 PRÓXIMAS FEATURES (AUTOMATICAMENTE PUBLICADAS)

```
Feature 6: → v1.1.0 (automático)
Feature 7: → v1.2.0 (automático)
Feature 8: → v1.3.0 (automático)
Bug fixes: → v1.0.1, v1.0.2, etc (automático)
```

**Sem precisar fazer nada manual! 🎉**

---

## ⏭️ PRÓXIMO PASSO

**Vamos implementar?**

Ordem recomendada:
1. Criar scripts (bump_version.py, generate_changelog.py)
2. Atualizar pyproject.toml
3. Criar GitHub Actions workflow
4. Configurar PyPI token
5. Testar tudo

**Tempo estimado: ~90 minutos**

Quer começar?
