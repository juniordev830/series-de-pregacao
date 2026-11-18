# Calendário de séries de pregação

Distribua sermões em datas semanais e pule dias reservados para outras atividades.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Use datas no formato ISO AAAA-MM-DD. A série começa na data indicada, progride com a cadência escolhida em semanas e pula datas que coincidam com eventos.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Levar a agenda para o calendário

Com Python e Node.js 18 ou superior, execute os comandos abaixo em um terminal
Bash. O primeiro calcula as datas e aplica os bloqueios. O segundo lê o
relatório e gera um evento de dia inteiro por mensagem, com a passagem bíblica
na descrição.

```sh
python app.py exemplo.json > agenda.json
node exportar-agenda.mjs < agenda.json > serie.ics
```

Importe `serie.ics` no seu aplicativo de calendário. No exemplo, as mensagens
ficam em 6 e 20 de dezembro porque o dia 13 está reservado.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar as datas e passagens da série. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.
