# ✨ Funcionalidades Implementadas - Discover Lisboa

## 📊 Checklist de Requisitos Académicos

### ✅ Backend (Python + Flask)
- [x] Framework Flask configurado
- [x] Base de dados SQLite
- [x] Arquitetura MVC (Models, Routes, Templates)
- [x] Sistema de sessões
- [x] API endpoints RESTful

### ✅ Sistema de Utilizadores
- [x] Registo com username e email
- [x] Validação de email obrigatória
- [x] Tokens seguros com expiração (24h)
- [x] Email enviado via SMTP (Gmail)
- [x] Definição de password após validação
- [x] Confirmação de password (dupla inserção)
- [x] Passwords encriptadas (bcrypt)
- [x] Login por username ou email
- [x] Sistema de sessões seguro
- [x] Logout funcional

### ✅ Gestão de Conteúdos
- [x] CRUD completo (Create, Read, Update, Delete)
- [x] Campos implementados:
  - Título
  - Descrição
  - Categoria (7 tipos)
  - Tipo de multimédia
  - Upload de ficheiros (imagem/vídeo/áudio)
  - Localização GPS (latitude/longitude)
  - Data de criação
- [x] Associação de conteúdos ao utilizador
- [x] Validação de formulários

### ✅ Categorias Disponíveis
1. Restaurante
2. Museu
3. Monumento
4. Miradouro
5. Ponto Turístico
6. Gastronomia
7. Outro

### ✅ Tipos de Multimédia
- Imagem (JPG, PNG, GIF)
- Vídeo (MP4, WEBM)
- Áudio (MP3, WAV)

### ✅ Mapa Interativo (Leaflet.js)
- [x] Integração com Leaflet
- [x] Base OpenStreetMap
- [x] Markers personalizados por categoria
- [x] Popups com:
  - Nome do local
  - Descrição
  - Categoria
  - Multimédia incorporada
- [x] Zoom e navegação interativa
- [x] Centrado em Lisboa (38.7223°N, 9.1393°W)

### ✅ Pesquisa Inteligente de Locais
- [x] Integração com Nominatim API (OpenStreetMap)
- [x] Pesquisa por nome do local
- [x] Obtenção automática de coordenadas GPS
- [x] Movimento automático do mapa
- [x] Marcador temporário no resultado
- [x] Implementado em 2 locais:
  1. No formulário de criação (autocomplete)
  2. No mapa principal (barra de pesquisa)

### ✅ Dashboard Privada
- [x] Acesso apenas após login
- [x] Estatísticas de conteúdos
- [x] Listagem de todos os conteúdos do utilizador
- [x] Pesquisa por nome/descrição
- [x] Filtro por categoria
- [x] Botões de ação:
  - Ver no mapa
  - Editar
  - Eliminar
- [x] Adição rápida com pesquisa de local
- [x] Link para criação de novo conteúdo

### ✅ Frontend (HTML5 + CSS3 + JavaScript)
- [x] HTML5 semântico
- [x] CSS3 moderno com:
  - Variáveis CSS
  - Flexbox e Grid
  - Animações e transições
  - Design responsivo
- [x] JavaScript vanilla (sem frameworks)
- [x] Interações assíncronas (Fetch API)

### ✅ Design Responsivo
- [x] Layout adaptativo para:
  - Desktop (>1024px)
  - Tablet (768px-1024px)
  - Mobile (<768px)
- [x] Menu hambúrguer em mobile
- [x] Grid responsivo
- [x] Imagens otimizadas

### ✅ Segurança Implementada
- [x] Passwords com hash bcrypt
- [x] Tokens seguros (secrets.token_urlsafe)
- [x] Proteção contra SQL injection (SQLAlchemy ORM)
- [x] Validação de ficheiros (tipo e tamanho)
- [x] Sessões seguras com SECRET_KEY
- [x] Proteção de rotas (login_required)
- [x] Expiração de tokens
- [x] Sanitização de inputs

### ✅ Funcionalidades Extra
- [x] Mini-mapa no formulário de criação
- [x] Clique no mapa para definir localização
- [x] Preview de multimédia antes de upload
- [x] Contadores e estatísticas
- [x] Mensagens flash (feedback ao utilizador)
- [x] Loading states
- [x] Validação em tempo real
- [x] Ordenação de conteúdos por data

## 🎯 Objetivos Académicos Cumpridos

### Programação Web Dinâmica
✅ Aplicação full-stack funcional  
✅ Interação cliente-servidor  
✅ Manipulação do DOM  
✅ Requisições assíncronas  

### Base de Dados
✅ Modelo relacional (3 tabelas)  
✅ Relações entre entidades  
✅ CRUD completo  
✅ Queries otimizadas  

### APIs Externas
✅ Nominatim API (geocodificação)  
✅ OpenStreetMap (mapas)  
✅ Gmail SMTP (emails)  

### Boas Práticas
✅ Código organizado e modular  
✅ Separação de concerns (MVC)  
✅ Comentários explicativos  
✅ Nomenclatura consistente  
✅ Gestão de erros  
✅ Validação de dados  

### Segurança
✅ Autenticação robusta  
✅ Encriptação de passwords  
✅ Proteção de rotas  
✅ Validação de inputs  
✅ Tokens seguros  

## 📈 Métricas do Projeto

- **Linhas de código**: ~2000+
- **Ficheiros**: 20+
- **Tabelas BD**: 3
- **Rotas**: 15+
- **Templates**: 9
- **APIs externas**: 3
- **Tecnologias**: 10+

## 🎓 Adequação ao Contexto Académico

Este projeto demonstra:

1. **Competências Técnicas**
   - Programação backend (Python/Flask)
   - Programação frontend (HTML/CSS/JS)
   - Gestão de bases de dados
   - Integração de APIs

2. **Pensamento Arquitetural**
   - Estrutura MVC
   - Separação de responsabilidades
   - Código escalável

3. **Resolução de Problemas**
   - Autenticação segura
   - Upload de ficheiros
   - Geolocalização
   - Pesquisa inteligente

4. **Aplicação Prática**
   - Caso de uso real (turismo)
   - UX pensada para utilizadores
   - Interface moderna e intuitiva

## 🚀 Possíveis Extensões Futuras

Para melhorar ainda mais (opcional):

- [ ] Sistema de comentários/reviews
- [ ] Avaliações com estrelas
- [ ] Partilha nas redes sociais
- [ ] Exportar itinerários em PDF
- [ ] Favoritos/wishlist
- [ ] Filtro por distância
- [ ] Modo escuro
- [ ] Múltiplos idiomas (i18n)
- [ ] PWA (Progressive Web App)
- [ ] Notificações push

## ✅ Conclusão

O projeto **Discover Lisboa** cumpre todos os requisitos obrigatórios da cadeira de Programação Web e demonstra competências avançadas em desenvolvimento full-stack, sendo adequado para avaliação académica ao nível de licenciatura em Engenharia Informática.
