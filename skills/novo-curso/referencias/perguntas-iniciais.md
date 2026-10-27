# Perguntas iniciais

Definem `src/config/definicao-curso.ts` do curso novo. Referência dos
campos: `DEFINICAO-CURSO.md` da base; para ver cada formato funcionando:
`?catalogo` → Formatos de curso (dev da base ou catálogo publicado).

Antes de perguntar, deduza o que der do roteiro e do layout (ex.: roteiro
com menu lateral → `menu.tipo: "lateral"` recomendado; slides 16:9 com
"avançar" → tela a tela) e pergunte só o que ficou em aberto, com
AskUserQuestion (até 4 por vez, a opção deduzida como "(Recomendado)").
Campo sem pergunta fica com o padrão da base.

As respostas viram o `definicao.json` passado ao script e a seção
"Course definition" do `CLAUDE.md` do curso (com o porquê das escolhas que
não forem óbvias).

## Perguntas

| # | Pergunta | Campo | Padrão |
| --- | --- | --- | --- |
| 1 | Rolagem ou tela a tela? | `navegacao` | `"rolagem"` |
| 2 | Quantos módulos? Com mais de um: começa num menu de módulos? Botão para voltar a ele? | `menuModulos` | `false` |
| 3 | Travas: cada interação trava o resto / só entre módulos / livre | `travas` | `"linear"` |
| 4 | Transição ao entrar num módulo: nenhuma / animação / vídeo (pode pular?) | `transicaoModulo` | `false` |
| 5 | (rolagem) Header fixo? Com título? Com progresso? | `header` | `false` |
| 6 | (rolagem) Menu: o da base (nenhum / lateral / flutuante; itens por tema ou por seção; com progresso; lateral começa aberto?) ou um menu próprio do cliente (`menu: false` + componente no curso)? | `menu` | `false` |
| 7 | (rolagem) Aviso "role a página" após inatividade? | `instrucaoRolagem` | `false` |
| 8 | (telas) Menu de salto no header? Setas do teclado? Tempo de leitura? | `telas.*` | sem menu, com setas, 3 s |
| 9 | Menu de acessibilidade? VLibras? | `acessibilidade` | menu sim, VLibras não |
| 10 | Conclusão: chegar ao fim / concluir todas as interações / nota | `conclusao` | `"fim"` |
| 11 | Avaliação final (obrigatória com nota): nº de questões, nota mínima, tentativas, sorteio | `avaliacaoFinal` | `false` |
| 12 | Idioma dos textos (pt-BR, en, es) | `idioma` | `"pt-BR"` |

Combinações inválidas não compilam (o script avisa no typecheck): botão de
voltar ao menu na rolagem exige `header`; conclusão por nota exige
`avaliacaoFinal`.

Número de módulos não é campo: o script cria o m01; os outros seguem o
`docs/guia-conteudo.md` do curso.

## Sem campo (anotar no `CLAUDE.md`)

- Vídeo em Libras nas seções → `libras` em `config/secoes.ts`.
- Legendas e transcrições → slots dos players.
- LMS de destino e restrições conhecidas (tamanho do pacote, iframe,
  fontes externas).

Fixos na base (não perguntar): SCORM 1.2, `plural-video`,
`plural-wavesurfer`, `?liberar` + `build:validacao`, catálogo. Gamificação
fica no curso.

## Exemplo de `definicao.json`

```json
{
	"navegacao": "rolagem",
	"menuModulos": { "voltarPeloHeader": true },
	"header": { "titulo": true, "progresso": true },
	"menu": { "tipo": "lateral", "itens": "grupos", "progresso": true }
}
```

Tela a tela: `{ "navegacao": "telas", "telas": { "menuSalto": true } }` (o
script completa o resto de `telas` e tira os campos de rolagem).
