// Captura cada seção do curso em desktop e celular, para comparar com o
// layout, e lista os erros/avisos do console.
//
// Uso (numa pasta com playwright instalado — ex.: <scratchpad>/pw, com
// `npm i playwright`; copie este arquivo para lá):
//   node capturar-secoes.mjs <url> <pasta-saida> [larguras] [seletor]
//   node capturar-secoes.mjs "http://localhost:5317/?liberar" ./capturas 1280,390
//
// - Use ?liberar para todas as seções estarem visíveis.
// - seletor padrão: '[id^="m0"][id*="s"]' (wrappers de seção do AppCoreSecoes, id mNNsM).
// - Saída: <pasta>/<largura>/<id>.png. Animações AOS são desligadas.
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

for (const largura of larguras.split(",").map(Number)) {
	const page = await browser.newPage({ viewport: { width: largura, height: 900 } });
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
	await page.close();
}

console.log(erros.size ? [...erros].join("\n") : "sem erros no console");
await browser.close();
