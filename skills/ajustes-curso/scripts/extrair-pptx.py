#!/usr/bin/env python3
"""Extrai, por slide, as caixas de texto, imagens, notas e comentários de um .pptx.

Uso: python3 extrair-pptx.py arquivo.pptx [pasta-saida]

Imprime um relatório em Markdown. Cada caixa de texto sai como um bloco
(`[caixa N]`), na ordem em que está no slide. Formatação relevante:
negrito `**x**` (vira <strong> no curso), riscado `~~x~~`, realce `==x==`;
quebras de linha viram ` / `.

Imagens são classificadas pelo tamanho no slide:
- `print da tela`: ocupa boa parte do slide — é o print do curso anotado;
- `referência`: imagem menor, normalmente dentro de uma caixa de anotação
  (o relatório diz qual). Serve só para entender o que o cliente quer —
  **nunca** vira asset do curso.

Se `pasta-saida` for informada, as imagens são salvas lá já com o recorte
aplicado no pptx (`slideNN-print.png` / `slideNN-ref-K.png`), para consulta
visual. Usa Pillow para recortar quando disponível.
"""

import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

try:
	from PIL import Image
except ImportError:  # recorte é opcional
	Image = None

NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"

# Fração da área do slide a partir da qual uma imagem é tratada como o print.
LIMIAR_PRINT = 0.35


def trecho(run):
	"""Texto de um <a:r>, marcando negrito, riscado e realce."""
	texto = "".join(t.text or "" for t in run.iter(f"{NS_A}t"))
	rpr = run.find(f"{NS_A}rPr")
	if not texto.strip() or rpr is None:
		return texto
	nucleo = texto.strip()
	if rpr.get("b") == "1":
		nucleo = f"**{nucleo}**"
	if rpr.get("strike", "noStrike") != "noStrike":
		nucleo = f"~~{nucleo}~~"
	if rpr.find(f"{NS_A}highlight") is not None:
		nucleo = f"=={nucleo}=="
	# Devolve os espaços das bordas fora da marcação.
	ini = texto[: len(texto) - len(texto.lstrip())]
	fim = texto[len(texto.rstrip()) :]
	return f"{ini}{nucleo}{fim}"


def paragrafos(raiz):
	"""Texto de cada parágrafo <a:p>, ignorando vazios."""
	saida = []
	for p in raiz.iter(f"{NS_A}p"):
		partes = []
		for el in p:
			if el.tag in (f"{NS_A}r", f"{NS_A}fld"):
				partes.append(trecho(el))
			elif el.tag == f"{NS_A}br":
				partes.append(" / ")
		texto = re.sub(r"\s+", " ", "".join(partes))
		texto = re.sub(r"\s/(\s*/)+\s", " / ", texto)
		# Junta negritos vizinhos: "**a** **b**" -> "**a b**".
		texto = re.sub(r"\*\*(\s*)\*\*", r"\1", texto).strip(" /")
		if texto:
			saida.append(texto)
	return saida


def rels(zf, caminho):
	"""Mapa rId -> (tipo, alvo absoluto no zip) do .rels de `caminho`."""
	pasta, nome = posixpath.split(caminho)
	arq = f"{pasta}/_rels/{nome}.rels"
	if arq not in zf.namelist():
		return {}
	mapa = {}
	for r in ET.fromstring(zf.read(arq)).iter(f"{NS_REL}Relationship"):
		alvo = r.get("Target")
		if r.get("TargetMode") != "External":
			alvo = posixpath.normpath(posixpath.join(pasta, alvo))
		mapa[r.get("Id")] = (r.get("Type").rsplit("/", 1)[-1], alvo)
	return mapa


def ordem_slides(zf):
	"""Slides na ordem da apresentação (não a do nome do arquivo) e a área do slide."""
	pres = ET.fromstring(zf.read("ppt/presentation.xml"))
	mapa = rels(zf, "ppt/presentation.xml")
	tam = pres.find(f"{NS_P}sldSz")
	area = int(tam.get("cx")) * int(tam.get("cy"))
	slides = [
		(mapa[s.get(f"{NS_R}id")][1], s.get("show") == "0")
		for s in pres.iter(f"{NS_P}sldId")
	]
	return slides, area


def caixa(el):
	"""(x, y, w, h) em EMU do primeiro <a:xfrm> do elemento, ou None."""
	xfrm = el.find(f".//{NS_A}xfrm")
	if xfrm is None or xfrm.find(f"{NS_A}off") is None:
		return None
	off, ext = xfrm.find(f"{NS_A}off"), xfrm.find(f"{NS_A}ext")
	return tuple(int(v) for v in (off.get("x"), off.get("y"), ext.get("cx"), ext.get("cy")))


def contem(externa, interna):
	"""A caixa `externa` contém o centro da `interna`?"""
	if not externa or not interna:
		return False
	cx = interna[0] + interna[2] / 2
	cy = interna[1] + interna[3] / 2
	return externa[0] <= cx <= externa[0] + externa[2] and externa[1] <= cy <= externa[1] + externa[3]


def formas(arvore):
	"""Percorre sp/pic do slide (inclusive dentro de grupos) na ordem do XML."""
	for el in arvore:
		if el.tag == f"{NS_P}grpSp":
			yield from formas(el)
		elif el.tag in (f"{NS_P}sp", f"{NS_P}pic"):
			yield el


def recorte(pic):
	"""Frações (l, t, r, b) cortadas da imagem original (<a:srcRect>)."""
	src = pic.find(f".//{NS_A}srcRect")
	if src is None:
		return (0, 0, 0, 0)
	return tuple(int(src.get(k, 0)) / 100000 for k in ("l", "t", "r", "b"))


def salvar_imagem(dados, corte, destino):
	"""Salva a imagem com o recorte do pptx aplicado (se houver Pillow)."""
	if Image is None or not any(corte):
		destino.write_bytes(dados)
		return
	img = Image.open(BytesIO(dados))
	w, h = img.size
	l, t, r, b = corte
	img.crop((round(w * l), round(h * t), round(w * (1 - r)), round(h * (1 - b)))).save(destino)


def comentarios(zf, alvo, nomes):
	"""Comentários antigos (p:cm/p:text) e modernos (respostas incluídas)."""
	raiz = ET.fromstring(zf.read(alvo))
	saida = []
	for cm in raiz.iter():
		if not cm.tag.endswith("}cm") and not cm.tag.endswith("}reply"):
			continue
		autor = nomes.get(cm.get("authorId"), cm.get("authorId") or "?")
		texto = [el.text for el in cm if el.tag.endswith("}text") and el.text]
		if not texto:
			txbody = next((el for el in cm if el.tag.endswith("}txBody")), None)
			texto = paragrafos(txbody) if txbody is not None else []
		if texto:
			prefixo = "↳ " if cm.tag.endswith("}reply") else ""
			saida.append(f"{prefixo}{autor}: {' / '.join(texto)}")
	return saida


def autores(zf):
	nomes = {}
	for arq in ("ppt/commentAuthors.xml", "ppt/authors.xml"):
		if arq in zf.namelist():
			for a in ET.fromstring(zf.read(arq)):
				nomes[a.get("id")] = a.get("name")
	return nomes


def main():
	if len(sys.argv) < 2:
		sys.exit(__doc__)
	pptx = Path(sys.argv[1])
	destino = Path(sys.argv[2]) if len(sys.argv) > 2 else None
	if destino:
		destino.mkdir(parents=True, exist_ok=True)

	with zipfile.ZipFile(pptx) as zf:
		nomes = autores(zf)
		slides, area_slide = ordem_slides(zf)
		print(f"# {pptx.name}\n")
		for n, (slide, oculto) in enumerate(slides, start=1):
			titulo = f"## Slide {n}" + (" (oculto)" if oculto else "")
			print(f"{titulo}  <!-- {posixpath.basename(slide)} -->\n")
			mapa = rels(zf, slide)
			arvore = ET.fromstring(zf.read(slide)).find(f".//{NS_P}spTree")

			caixas, imagens = [], []
			for el in formas(arvore):
				if el.tag == f"{NS_P}sp":
					linhas = paragrafos(el)
					if linhas:
						caixas.append((caixa(el), linhas))
				else:
					blip = el.find(f".//{NS_A}blip")
					rid = blip.get(f"{NS_R}embed") if blip is not None else None
					if rid in mapa:
						imagens.append((caixa(el), mapa[rid][1], recorte(el)))

			for i, (_, linhas) in enumerate(caixas, start=1):
				print(f"**[caixa {i}]**")
				for linha in linhas:
					print(f"- {linha}")
				print()

			refs = 0
			for geo, alvo, corte in imagens:
				if alvo not in zf.namelist():
					print(f"- imagem externa: {alvo}")
					continue
				fracao = geo[2] * geo[3] / area_slide if geo else 0
				if fracao >= LIMIAR_PRINT:
					papel, nome = "print da tela", f"slide{n:02d}-print.png"
				else:
					refs += 1
					papel, nome = "referência", f"slide{n:02d}-ref-{refs}.png"
					dono = next(
						(i for i, (g, _) in enumerate(caixas, start=1) if contem(g, geo)),
						None,
					)
					if dono:
						papel += f" (dentro da caixa {dono})"
				if destino:
					salvar_imagem(zf.read(alvo), corte, destino / nome)
					print(f"- {papel}: `{nome}`")
				else:
					print(f"- {papel}: {posixpath.basename(alvo)}")

			notas, coments = [], []
			for tipo, alvo in mapa.values():
				if tipo == "notesSlide":
					raiz = ET.fromstring(zf.read(alvo))
					# Só o placeholder do corpo das notas (ignora nº do slide).
					for sp in raiz.iter(f"{NS_P}sp"):
						ph = sp.find(f".//{NS_P}ph")
						if ph is not None and ph.get("type") == "body":
							notas += paragrafos(sp)
				elif "omment" in tipo:
					coments += comentarios(zf, alvo, nomes)
			if notas:
				print("\n**Notas:**")
				for linha in notas:
					print(f"- {linha}")
			if coments:
				print("\n**Comentários:**")
				for c in coments:
					print(f"- {c}")
			print()


if __name__ == "__main__":
	main()
