/**
 * Tuinapp – webapp-endpoint op de Google Sheet "Tuinapp".
 * GET  : alle tabbladen die de app nodig heeft, als weergegeven tekst.
 * POST : afvinken (Voortgang), werkelijke stand (Stand) en eigen foto's (Fotos). Vereist de sleutel
 *        uit Scripteigenschappen (SLEUTEL). Installatie: zie README.md.
 */
const LEES = ['Locaties', 'Acties', 'Plekken', 'Planten', 'Beplanting', 'Regels', 'Projecttaken', 'Info', 'Stand', 'Voortgang', 'Instellingen', 'Fotos'];

function doGet(e) {
  const ss = SpreadsheetApp.getActive();
  const vraag = e && e.parameter && e.parameter.tabs ? e.parameter.tabs.split(',') : LEES;
  const tabs = {};
  vraag.filter(n => LEES.indexOf(n) >= 0).forEach(n => { tabs[n] = waarden_(ss, n); });
  return uit_({ ok: true, tijd: new Date().toISOString(), tabs: tabs });
}

function doPost(e) {
  let b;
  try { b = JSON.parse(e.postData.contents); } catch (x) { return uit_({ ok: false, fout: 'ongeldige invoer' }); }
  const sleutel = PropertiesService.getScriptProperties().getProperty('SLEUTEL');
  if (!sleutel || b.sleutel !== sleutel) return uit_({ ok: false, fout: 'sleutel' });
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const ss = SpreadsheetApp.getActive();
    (b.acties || []).forEach(a => voerUit_(ss, a));
    SpreadsheetApp.flush();
    return uit_({ ok: true, tijd: new Date().toISOString(), tabs: { Stand: waarden_(ss, 'Stand'), Voortgang: waarden_(ss, 'Voortgang'), Fotos: waarden_(ss, 'Fotos') } });
  } catch (x) {
    return uit_({ ok: false, fout: String(x) });
  } finally {
    lock.releaseLock();
  }
}

function voerUit_(ss, a) {
  const zelfde = (r, taak, jaar) => r.taak === taak && String(r.jaar) === String(jaar);
  switch (a.op) {
    case 'voortgang_aan': verwijder_(ss, 'Voortgang', r => zelfde(r, a.rij.taak, a.rij.jaar)); voegToe_(ss, 'Voortgang', a.rij); break;
    case 'voortgang_uit': verwijder_(ss, 'Voortgang', r => zelfde(r, a.taak, a.jaar)); break;
    case 'stand_zet': verwijder_(ss, 'Stand', r => r.key === a.rij.key); voegToe_(ss, 'Stand', a.rij); break;
    case 'stand_weg': verwijder_(ss, 'Stand', r => r.key === a.key); break;
    case 'foto_zet': verwijder_(ss, 'Fotos', r => r.key === a.rij.key); voegToe_(ss, 'Fotos', a.rij); break;
    case 'stand_weg_via': if (a.via_regel) verwijder_(ss, 'Stand', r => r.via_regel === a.via_regel); break;
  }
}

function waarden_(ss, naam) {
  const sh = ss.getSheetByName(naam);
  return sh ? sh.getDataRange().getDisplayValues().filter(r => r.some(c => c !== '')) : [];
}

function verwijder_(ss, naam, past) {
  const sh = ss.getSheetByName(naam);
  const w = sh.getDataRange().getDisplayValues();
  const kop = w[0];
  for (let i = w.length - 1; i >= 1; i--) {
    const r = {};
    kop.forEach((k, j) => { r[k] = w[i][j]; });
    if (past(r)) sh.deleteRow(i + 1);
  }
}

function voegToe_(ss, naam, rij) {
  const sh = ss.getSheetByName(naam);
  const kop = sh.getRange(1, 1, 1, sh.getLastColumn()).getDisplayValues()[0];
  const rng = sh.getRange(sh.getLastRow() + 1, 1, 1, kop.length);
  rng.setNumberFormat('@').setValues([kop.map(k => rij[k] == null ? '' : String(rij[k]))]);
}

function uit_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
