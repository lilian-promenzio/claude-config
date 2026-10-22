// Captura cada seção do curso (módulo atual) para comparar com o layout, e
// lista os erros/avisos do console.
//
// Uso (numa pasta com playwright instalado — ex.: <scratchpad>/pw, com
// `npm i playwright`; copie este arquivo para lá):
//   node capturar-secoes.mjs <url> <pasta-saida> [larguras] [seletor]
//   node capturar-secoes.mjs "http://localhost:5173/?liberar" ./capturas 1280,390
//
// - Use ?liberar para todas as seções estarem visíveis.
// - Rolagem: uma captura por seção (id mNNsM) em cada largura.
// - Tela a tela (detectado sozinho): janela do tamanho do canvas (escala 1),
//   uma captura por tela, avançando pelo botão; larguras ignoradas.
// - Saída: <pasta>/<largura ou "telas">/<id>.png. Animações de entrada
//   desligadas (prefers-reduced-motion; AOS nos cursos antigos).
// - CHROME: usa /usr/bin/google-chrome se existir (sem `npx playwright install`).
import { existsSync, mkdirSync } from "node:fs";
import { chromium } from "playwright";

const [url, saida, larguras = "1280,390", seletor = '[id^="m0"][id*="s"]'] = process.argv.slice(2);
if (!url || !saida) {
	console.error("uso: node capturar-secoes.mjs <url> <pasta-saida> [larguras] [seletor]");
	process.exit(1);
}

const chrome = "/usr/bin/google-chrome";
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});
const erros = new Set();

async function abrir(viewport) {
	const page = await browser.newPage({ viewport, reducedMotion: "reduce" });
	page.on("console", (m) => {
		if (["error", "warning"].includes(m.type())) erros.add(`[${m.type()}] ${m.text()}`);
	});
	page.on("pageerror", (e) => erros.add(`[pageerror] ${e.message}`));
	page.on("response", (r) => {
		if (r.status() >= 400) erros.add(`[${r.status()}] ${r.url()}`);
	});
	await page.goto(url, { waitUntil: "networkidle" });
	await page.addStyleTag({
		content: "[data-aos]{opacity:1!important;transform:none!important;transition:none!important}",
	});
	return page;
}

async function capturarTelas(page) {
	// Canvas em escala 1: janela do tamanho dele
	const canvas = await page.locator(".casca-telas__canvas").evaluate((el) => ({
		width: Number.parseInt(el.style.width),
		height: Number.parseInt(el.style.height),
	}));
	await page.setViewportSize(canvas);
	await page.waitForTimeout(300);

	const pasta = `${saida}/telas`;
	mkdirSync(pasta, { recursive: true });
	const vistas = new Set();
	for (;;) {
		const secao = page.locator(".casca-telas__secao");
		const id = (await secao.count()) ? await secao.getAttribute("id") : "menu";
		if (vistas.has(id)) break;
		vistas.add(id);
		await page.locator(".app-tela-palco__tela").screenshot({ path: `${pasta}/${id}.png` });
		const avancar = page.locator(".app-tela-palco__botao--avancar");
		if ((await avancar.count()) === 0 || (await avancar.isDisabled())) break;
		await avancar.click();
		await page.waitForTimeout(400);
	}
	console.log(`telas: ${vistas.size} capturas em ${pasta}`);
}

async function capturarRolagem(page, largura) {
	const pasta = `${saida}/${largura}`;
	mkdirSync(pasta, { recursive: true });
	const ids = await page.$$eval(seletor, (els) => els.map((el) => el.id));
	for (const id of ids) {
		const el = page.locator(`[id="${id}"]`);
		await el.scrollIntoViewIfNeeded();
		await page.waitForTimeout(300);
		await el.screenshot({ path: `${pasta}/${id}.png` });
	}
	console.log(`${largura}px: ${ids.length} seções em ${pasta}`);

	// rolagem horizontal indesejada
	const vaza = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
	if (vaza) erros.add(`[layout] rolagem horizontal em ${largura}px`);
}

const primeira = await abrir({ width: 1600, height: 900 });
const telas = await primeira.evaluate(() => document.documentElement.dataset.navegacao === "telas");
if (telas) {
	await capturarTelas(primeira);
	await primeira.close();
} else {
	await primeira.close();
	for (const largura of larguras.split(",").map(Number)) {
		const page = await abrir({ width: largura, height: 900 });
		await capturarRolagem(page, largura);
		await page.close();
	}
}

console.log(erros.size ? [...erros].join("\n") : "sem erros no console");
await browser.close();
