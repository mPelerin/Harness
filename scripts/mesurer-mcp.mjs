// Mesure la liste d'outils d'un serveur MCP local (stdio), sans client IA.
// Usage : node scripts/mesurer-mcp.mjs <nom> -- <commande> [arguments...]
// Le serveur est lancé, on lit sa liste d'outils, puis on l'arrête avec tous ses sous-processus.
// Les jetons sont estimés à 4 octets par jeton : c'est un ordre de grandeur, pas un compte exact.
import { spawn } from 'node:child_process';

const sep = process.argv.indexOf('--');
const nom = process.argv[2];
const cmd = process.argv.slice(sep + 1);
if (sep < 0 || cmd.length === 0) {
  console.log('STOP usage : node scripts/mesurer-mcp.mjs <nom> -- <commande> [arguments...]');
  process.exit(1);
}

const p = spawn(cmd[0], cmd.slice(1), { stdio: ['pipe', 'pipe', 'pipe'], detached: true });
let tampon = '';
let fini = false;

function arreter() {
  try { process.kill(-p.pid, 'SIGTERM'); } catch {}
  setTimeout(() => { try { process.kill(-p.pid, 'SIGKILL'); } catch {} }, 1500);
}
function fin(message, code) {
  if (fini) return;
  fini = true;
  clearTimeout(minuterie);
  console.log(message);
  arreter();
  setTimeout(() => process.exit(code), 2000);
}
function envoyer(objet) {
  p.stdin.write(JSON.stringify(objet) + '\n');
}

const minuterie = setTimeout(() => fin(`STOP ${nom} : pas de réponse en 180 s`, 1), 180000);

p.stdout.on('data', (morceau) => {
  tampon += morceau;
  let k;
  while ((k = tampon.indexOf('\n')) >= 0) {
    const ligne = tampon.slice(0, k).trim();
    tampon = tampon.slice(k + 1);
    if (!ligne) continue;
    let m;
    try { m = JSON.parse(ligne); } catch { continue; }
    if (m.id === 1) {
      envoyer({ jsonrpc: '2.0', method: 'notifications/initialized' });
      envoyer({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
    } else if (m.id === 2) {
      const outils = (m.result && m.result.tools) || [];
      const octets = Buffer.byteLength(JSON.stringify(outils));
      fin(`OK ${nom} : ${outils.length} outils, ${octets} octets, environ ${Math.round(octets / 4)} jetons | ${outils.map((o) => o.name).join(' ')}`, 0);
    }
  }
});
p.stderr.on('data', () => {});
p.on('error', (e) => fin(`STOP ${nom} : lancement impossible (${e.message})`, 1));
p.on('exit', (c) => fin(`STOP ${nom} : le serveur s'est arrêté avant de répondre (code ${c})`, 1));

envoyer({
  jsonrpc: '2.0', id: 1, method: 'initialize',
  params: { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'mesure-harness', version: '1' } },
});
