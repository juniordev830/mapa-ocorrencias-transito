# Registro de ocorrências de trânsito

Filtre registros locais de obras, alagamentos e bloqueios por data de validade.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

As ocorrências do exemplo são fictícias. Informe sua data de consulta e as datas de início e fim de cada ocorrência, inclusive. O programa ordena as ativas por gravidade e oferece um link de mapa por ponto.

## Google Maps

Os links seguem a documentação de [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) e abrem o app ou site sem chave. Confira no Maps a rota oferecida, a cobertura de transporte e as condições do momento. Os valores numéricos no arquivo de exemplo são demonstrações.

## Estado do projeto

Versão inicial funcional por linha de comando, sem interface web. Usa apenas a biblioteca padrão do Python. Os testes executam os exemplos e verificam as regras do projeto.
