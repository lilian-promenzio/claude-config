# Perguntas iniciais (FUTURO)

> **Ainda não usar.** Este questionário só faz sentido quando existir a base
> Plural genérica, com cada recurso abaixo disponível como opção de liga e
> desliga. Enquanto o projeto parte de um curso de referência (modo A do
> `SKILL.md`), os recursos vêm da própria referência.

Quando ativo: antes de criar o projeto, faça estas perguntas ao usuário (use
AskUserQuestion, agrupando no máximo 4 por vez). Antes, preencha o que der
para deduzir do roteiro e do layout (ex.: o roteiro mostra um menu lateral →
sugerir "menu lateral com âncoras e progresso" como recomendado) e pergunte
só o que ficar em aberto. Registre as respostas no `CLAUDE.md` do novo
projeto, em "Definições do curso".

## Estrutura e navegação

1. **Navegação**
   - *One page*: módulo único com seções empilhadas e rolagem contínua.
   - *Multipage*: vários módulos, com menu/tela de módulos.
   - *Tela a tela*: uma seção por tela, com navegação linear
     (avançar/voltar).
2. **Travas**: toda interação trava o que vem depois (padrão) / navegação
   livre / travas só entre módulos.
3. **Menu de âncoras flutuante** (atalhos para os temas, sem progresso):
   sim / não.
4. **Menu lateral com âncoras e progresso** (colapsável, links liberados
   conforme o avanço, barra de progresso da peça): sim / não.
5. **Cabeçalho fixo** (logo, título, progresso): sim / não.

## Acessibilidade

6. **Plugin de acessibilidade** (contraste, tamanho de fonte, etc.): sim /
   não.
7. **Plugin VLibras**: sim / não.
8. **Libras em vídeo** (intérprete nos vídeos ou nas seções): sim / não.
9. **Legendas e transcrições** de vídeo e áudio: legendas / transcrição /
   ambas / nenhuma.

## Conclusão e avaliação

10. **Padrão SCORM**: 1.2 (padrão) / 2004.
11. **Critério de conclusão**: chegar ao fim / concluir todas as interações /
    nota mínima na avaliação.
12. **Avaliação final**: não / sim (nº de questões, nota mínima, tentativas,
    sorteio de questões).
13. **Gamificação**: conquistas, pontos ou perfil final (ex.: mini game).

## Conteúdo e mídia

14. **Idiomas**: só pt-BR / multilíngue (quais).
15. **Player de vídeo**: padrão da base / do LMS / YouTube ou Vimeo.
16. **Podcast/áudio**: player com forma de onda (`plural-wavesurfer`) /
    player simples.
17. **Materiais para download** (PDF, links): sim / não.

## Entrega e validação

18. **Build de validação com `?liberar`** para revisão do cliente: sim
    (padrão) / não.
19. **LMS de destino** (se houver restrições conhecidas: tamanho do pacote,
    iframe, bloqueio de fontes externas).
20. **Catálogo de componentes** (`/?catalogo` em dev): sim (padrão) / não.

Acrescente perguntas aqui sempre que um novo recurso opcional entrar na
base.
