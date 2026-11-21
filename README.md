# Registro de ocorrências de trânsito

Filtre registros locais de obras, alagamentos e bloqueios por data de validade.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

As datas devem ser datas reais do calendário, no formato `AAAA-MM-DD` (por exemplo, `2026-11-15`); formatos compactos, dias impossíveis e separadores alternativos são rejeitados.\n\nAs ocorrências do exemplo são fictícias. Informe sua data de consulta e as datas de início e fim de cada ocorrência, inclusive. O programa ordena as ativas por gravidade e oferece um link de mapa por ponto.

## Google Maps

Os links seguem a documentação de [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) e abrem o app ou site sem chave. Confira no Maps a rota oferecida, a cobertura de transporte e as condições do momento. Os valores numéricos no arquivo de exemplo são demonstrações.

## Estado do projeto

Versão inicial funcional por linha de comando, sem interface web. Usa apenas a biblioteca padrão do Python. Os testes executam os exemplos e verificam as regras do projeto.

Use o campo opcional `gravidade_minima` na entrada para exibir somente ocorrências ativas com gravidade igual ou superior ao valor informado, de 1 a 3. O padrão é 1.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar as ocorrências ativas por gravidade. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```
