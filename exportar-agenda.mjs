import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

function texto(valor) {
  if (typeof valor !== 'string' || !valor.trim() ||
      /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/u.test(valor)) {
    throw new Error('Título ou referência inválida.');
  }
  return valor.replace(/\\/g, '\\\\').replace(/\r\n|\r|\n/g, '\\n')
    .replace(/,/g, '\\,').replace(/;/g, '\\;');
}

function linhasFisicas(linha) {
  const partes = [];
  let atual = '';
  let bytes = 0;
  for (const caractere of linha) {
    const tamanho = Buffer.byteLength(caractere);
    if (bytes + tamanho > 75) {
      partes.push(atual);
      atual = ' ';
      bytes = 1;
    }
    atual += caractere;
    bytes += tamanho;
  }
  partes.push(atual);
  return partes;
}

function calendario(relatorio) {
  if (!Array.isArray(relatorio?.agenda)) throw new Error('O relatório deve conter uma agenda.');
  const revisao = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  const linhas = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Series de Pregacao//Agenda//PT-BR'];
  for (const evento of relatorio.agenda) {
    const { data, titulo, referencia } = evento;
    if (typeof data !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(data)) {
      throw new Error('Data fora do formato AAAA-MM-DD.');
    }
    const instante = new Date(data + 'T00:00:00Z');
    if (Number.isNaN(instante.valueOf()) || instante.toISOString().slice(0, 10) !== data) {
      throw new Error('Data inexistente no calendário.');
    }
    const resumo = texto(titulo);
    const passagem = texto(referencia);
    const id = createHash('sha256').update(JSON.stringify([data, titulo, referencia])).digest('hex');
    linhas.push('BEGIN:VEVENT', 'UID:' + id + '@series-de-pregacao',
      'DTSTAMP:' + revisao, 'DTSTART;VALUE=DATE:' + data.replace(/-/g, ''),
      'SUMMARY:' + resumo, 'DESCRIPTION:' + passagem, 'END:VEVENT');
  }
  linhas.push('END:VCALENDAR');
  return linhas.flatMap(linhasFisicas).join('\r\n') + '\r\n';
}

try {
  const relatorio = JSON.parse(readFileSync(0, 'utf8').replace(/^\uFEFF/, ''));
  process.stdout.write(calendario(relatorio));
} catch (erro) {
  process.stderr.write('Erro ao exportar a agenda: ' + erro.message + '\n');
  process.exitCode = 2;
}
