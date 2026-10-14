#!/usr/bin/env python3
"""Extrai o texto de um roteiro .pptx preservando a formatação que o curso
precisa reproduzir.

Uso: python3 extrair-roteiro.py roteiro.pptx > roteiro.md

Sem dependências (só a biblioteca padrão). Para cada slide, imprime as formas
em ordem de leitura (de cima para baixo, da esquerda para a direita), com a
posição em % do slide, e cada parágrafo já em HTML inline:

- negrito → <strong>, itálico → <em>, sublinhado → <u>, riscado → <s>
- caixa alta aplicada por ESTILO (cap="all", o texto foi digitado em
  minúsculas) sai já em maiúsculas e marcada com [caps]: no curso, escrever
  as maiúsculas no próprio texto (nunca text-transform)
- tamanho da fonte em pt [24pt], quando definido no trecho — ajuda a ler a
  hierarquia de títulos
- marcadores de lista: "•" (buChar), "1." (buAutoNum), com recuo pelo nível
- tabelas viram linhas "| a | b |"
- imagens: nome e texto alternativo da forma (ex.: IMG_SLIDE_20)
- notas do slide no fim

Limitação: marcadores e tamanhos herdados do layout/mestre do pptx não
aparecem (só o que está explícito no slide). Confira a hierarquia também no
PDF do roteiro (soffice --headless --convert-to pdf).
"""

import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def esc(texto):
	return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def estilo(rpr):
	"""Formatação de um trecho: (tags, caps, tamanho)."""
	if rpr is None:
		return ((), False, None)
	tags = []
	if rpr.get("b") == "1":
		tags.append("strong")
	if rpr.get("i") == "1":
		tags.append("em")
	if rpr.get("u", "none") != "none":
		tags.append("u")
	if rpr.get("strike", "noStrike") != "noStrike":
		tags.append("s")
	caps = rpr.get("cap") == "all"
	sz = rpr.get("sz")
	return (tuple(tags), caps, int(sz) // 100 if sz else None)


def paragrafo(p):
	"""Um <a:p> em HTML inline, juntando trechos vizinhos de mesmo estilo."""
	blocos = []  # [estilo, texto]
	for el in p:
		if el.tag == f"{A}r" or el.tag == f"{A}fld":
			texto = "".join(t.text or "" for t in el.iter(f"{A}t"))
			est = estilo(el.find(f"{A}rPr"))
		elif el.tag == f"{A}br":
			texto, est = "\n", blocos[-1][0] if blocos else ((), False, None)
		else:
			continue
		if not texto:
			continue
		if blocos and blocos[-1][0] == est:
			blocos[-1][1] += texto
		else:
			blocos.append([est, texto])

	partes, tem_caps, tamanhos = [], False, set()
	for (tags, caps, sz), texto in blocos:
		if caps:
			texto, tem_caps = texto.upper(), True
		if sz and texto.strip():
			tamanhos.add(sz)
		html = esc(texto).replace("\n", "<br>")
		nucleo = html.strip()
		if tags and nucleo:
			ini = html[: len(html) - len(html.lstrip())]
			fim = html[len(html.rstrip()) :]
			abre = "".join(f"<{t}>" for t in tags)
			fecha = "".join(f"</{t}>" for t in reversed(tags))
			html = f"{ini}{abre}{nucleo}{fecha}{fim}"
		partes.append(html)
	html = re.sub(r"^(\s|<br>)+|(\s|<br>)+$", "", "".join(partes))
	if not html:
		return None

	ppr = p.find(f"{A}pPr")
	nivel = int(ppr.get("lvl", "0")) if ppr is not None else 0
	marcador = ""
	if ppr is not None:
		if ppr.find(f"{A}buAutoNum") is not None:
			marcador = "1. "
		elif ppr.find(f"{A}buChar") is not None:
			marcador = "• "
	extras = []
	if tamanhos:
		extras.append("/".join(f"{t}pt" for t in sorted(tamanhos, reverse=True)))
	if tem_caps:
		extras.append("caps")
	sufixo = f"  [{', '.join(extras)}]" if extras else ""
	return f"{'  ' * nivel}{marcador}{html}{sufixo}"


def texto_corpo(corpo):
	return [l for l in (paragrafo(p) for p in corpo.iter(f"{A}p")) if l]


def posicao(el, cx, cy):
	off = el.find(f".//{A}xfrm/{A}off")
	ext = el.find(f".//{A}xfrm/{A}ext")
	if off is None or ext is None:
		return (0, 0, 0, 0)
	return (
		int(off.get("x")) / cx * 100,
		int(off.get("y")) / cy * 100,
		int(ext.get("cx")) / cx * 100,
		int(ext.get("cy")) / cy * 100,
	)


def formas(arvore, cx, cy, nivel=0):
	"""Linhas do relatório para as formas de um spTree/grpSp."""
	itens = []
	for el in arvore:
		tag = el.tag.rsplit("}", 1)[-1]
		if tag not in ("sp", "pic", "grpSp", "graphicFrame"):
			continue
		cnv = el.find(f".//{P}cNvPr")
		nome = cnv.get("name", "") if cnv is not None else ""
		descr = cnv.get("descr", "") if cnv is not None else ""
		x, y, w, h = posicao(el, cx, cy)
		cab = f"{'  ' * nivel}- **{tag}** `{nome}` ({x:.0f}%, {y:.0f}% · {w:.0f}×{h:.0f}%)"
		linhas = []
		if tag == "sp":
			corpo = el.find(f"{P}txBody")
			linhas = texto_corpo(corpo) if corpo is not None else []
			if not linhas:
				continue  # formas decorativas sem texto
		elif tag == "pic":
			if descr:
				cab += f" — alt: {descr}"
		elif tag == "graphicFrame":
			for tr in el.iter(f"{A}tr"):
				celulas = [" / ".join(texto_corpo(tc)) for tc in tr.iter(f"{A}tc")]
				linhas.append("| " + " | ".join(celulas) + " |")
		elif tag == "grpSp":
			filhos = formas(el, cx, cy, nivel + 1)
			if not filhos:
				continue
			itens.append(((y, x), [cab] + [f for _, bloco in filhos for f in bloco]))
			continue
		recuo = "  " * (nivel + 1)
		itens.append(((y, x), [cab] + [f"{recuo}{l}" for l in linhas]))
	itens.sort(key=lambda item: (round(item[0][0]), item[0][1]))
	return itens


def main():
	if len(sys.argv) < 2:
		sys.exit(__doc__)
	zf = zipfile.ZipFile(sys.argv[1])
	pres = ET.fromstring(zf.read("ppt/presentation.xml"))
	tam = pres.find(f"{P}sldSz")
	cx, cy = int(tam.get("cx")), int(tam.get("cy"))

	rels = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
	alvos = {r.get("Id"): r.get("Target") for r in rels.iter(f"{REL}Relationship")}
	slides = [
		posixpath.normpath(posixpath.join("ppt", alvos[s.get(f"{R}id")]))
		for s in pres.iter(f"{P}sldId")
	]

	print(f"# Roteiro: {sys.argv[1]}\n")
	for n, caminho in enumerate(slides, 1):
		xml = ET.fromstring(zf.read(caminho))
		oculto = " (OCULTO)" if xml.get("show") == "0" else ""
		print(f"## Slide {n}{oculto}\n")
		for _, bloco in formas(xml.find(f"{P}cSld/{P}spTree"), cx, cy):
			print("\n".join(bloco))
		# notas
		rels_slide = posixpath.join(
			posixpath.dirname(caminho), "_rels", posixpath.basename(caminho) + ".rels"
		)
		if rels_slide in zf.namelist():
			for r in ET.fromstring(zf.read(rels_slide)).iter(f"{REL}Relationship"):
				if r.get("Type", "").endswith("/notesSlide"):
					notas = posixpath.normpath(
						posixpath.join(posixpath.dirname(caminho), r.get("Target"))
					)
					corpo = ET.fromstring(zf.read(notas))
					linhas = [
						l
						for sp in corpo.iter(f"{P}sp")
						if (sp.find(f".//{P}ph") is None or sp.find(f".//{P}ph").get("type") == "body")
						for l in (texto_corpo(sp) if sp.find(f"{P}txBody") is not None else [])
					]
					if linhas:
						print("\n**Notas:**\n" + "\n".join(f"> {l}" for l in linhas))
		print()


if __name__ == "__main__":
	main()
