# Laboratório 9 - Testes de Mutação

Simulação e Teste de Software (CC8550) - FEI

## Exercício 1 - Situação do Aluno

**a) Cobertura e mutmut (suíte inicial, 2 testes)**

| Cobertura de ramos | Gerados | Mortos | Vivos | MS |
|---|---|---|---|---|
| 64% (faltam as linhas 3, 5, 7 e 11) | 36 | 6 | 30 | 6/36 = 17% |

**b) Vivos agrupados pela causa**

| Causa | Mutantes | Qtd | Linha executada? |
|---|---|---|---|
| Mensagem do erro de média (None, XX, minúscula, maiúscula) | 6 a 9 | 4 | não (linha 3) |
| Mensagem do erro de presença | 15 a 18 | 4 | não (linha 5) |
| Texto "Reprovado por falta" | 21 a 23 | 3 | não (linha 7) |
| Texto "Recuperacao" | 31 a 33 | 3 | não (linha 11) |
| Fronteira da média inválida (`and`, `<=`, `<1`, `>=`, `>11`) | 1 a 5 | 5 | sim, mas sem entrada na fronteira |
| Fronteira da presença inválida | 10 a 14 | 5 | sim, mas sem entrada na fronteira |
| Fronteira da presença 75 (`<= 75`, `< 76`) | 19, 20 | 2 | sim |
| Fronteira da média 7.0 (`> 7.0`, `>= 8.0`) | 24, 25 | 2 | sim |
| Fronteira da média 5.0 (`> 5.0`, `>= 6.0`) | 29, 30 | 2 | sim |

Das 30 vivas, 14 estão em linhas que a suíte nem executa (as 4 linhas acima da cobertura). As outras 16 estão em decisões que são executadas, mas só com valores longe da fronteira.

**c) Testes novos**

Testes de média inválida (-0.1 e 10.1), presença inválida (-1 e 101), conferindo a mensagem exata, e uma tabela de limites: média 0, 10, 6.9, 7.0, 5.0, 4.9 e presença 0, 74, 75, 100.

| Cobertura de ramos | Gerados | Mortos | Vivos | Equivalentes | MS final |
|---|---|---|---|---|---|
| 100% | 36 | 36 | 0 | 0 | 36/36 = 100% |

Nenhum mutante é equivalente: todos mudam a saída para alguma entrada válida (ou o erro lançado) e foram mortos por algum teste.

**d) Trocando a conferência por `pytest.raises(ValueError, match=msg)`**

Com o `match`, ficaram 34 mortos e 2 vivos (MS = 34/36 = 94%). Os vivos são o mutante 7 (`"XXMedia invalidaXX"`) e o 16 (`"XXPresenca invalidaXX"`).

O `match` usa `re.search`, ou seja, só procura o texto dentro da mensagem. Se a mensagem tiver coisa a mais antes ou depois, ele ainda passa. Já o `str(erro.value) == msg` exige a mensagem inteira igual. Para o `match` ficar tão rígido quanto o `==`, dá pra usar `match="^Media invalida$"`.

---

## Exercício 2 - Desconto Progressivo

**a) Suíte inicial (`assert total_com_desconto([10, 20, 30, 40, 50]) > 0`)**

| Cobertura de ramos | Gerados | Mortos | Vivos | MS |
|---|---|---|---|---|
| 100% | 16 | 4 | 12 | 4/16 = 25% |

A cobertura diz que todo o código foi executado, mas o MS mostra que quase nada foi conferido. O `> 0` aceita quase qualquer erro de cálculo.

**b) Assert trocado por `== 141`** (10 + 20 + 30 + 40 x 0,9 + 50 x 0,9 = 141)

Sobram 3 vivos: mutantes 13, 15 e 16, todos na linha do `round`. MS = 13/16 = 81%.

**c) Condição que falhou em cada vivo**

| Mutante | Mudança | Condição que falhou |
|---|---|---|
| 13 | `round(total, None)` | infectar |
| 15 | `round(total, )` | infectar |
| 16 | `round(total, 3)` | infectar |

A linha do `round` é alcançada em todos. Mas o total é 141.0, que não tem casas decimais, então arredondar com 2, 3 ou 0 casas dá o mesmo valor. A entrada não faz diferença entre as versões.

**d) Teste novo**

`total_com_desconto([10, 20, 30, 10.55]) == 69.5`

| Cobertura de ramos | Gerados | Mortos | Vivos | MS final |
|---|---|---|---|---|
| 100% | 16 | 16 | 0 | 100% |

Foi preciso um preço com centavos (10.55). Com o desconto vira 9.495, que é arredondado para 9.5 no original. O `round(total, 3)` deixa 69.495 e o arredondamento sem casas dá 69, então os três morrem.

---

## Exercício 3 - Temperaturas da Semana

**a) Suíte inicial (listas [21, 25, 19, 30, 22], [18], [30, 21] e lista vazia, para as duas funções)**

Cobertura de ramos 100%. 22 mutantes gerados, 11 mortos e 11 vivos.

Vivos (mutmut show):

| Mutante | Mudança |
|---|---|
| maior_2, 3, 4 | mensagem `None`, `"XXlista vaziaXX"`, `"LISTA VAZIA"` |
| maior_7 | `temps[1:]` vira `temps[2:]` |
| maior_8 | `t > m` vira `t >= m` |
| dia_do_maior_2, 3, 4 | mensagem `None`, `"XXlista vaziaXX"`, `"LISTA VAZIA"` |
| dia_do_maior_9 | `range(1, len(temps))` vira `range(len(temps))` |
| dia_do_maior_11 | `range(1, ...)` vira `range(2, ...)` |
| dia_do_maior_12 | `temps[i] > temps[pos]` vira `>=` |

**b) Classificação**

| Mutante | Equivalente? | Justificativa |
|---|---|---|
| maior_2, 3, 4 e dia_do_maior_2, 3, 4 | não | a mensagem muda e dá pra conferir no teste |
| maior_7 | não | se o maior estiver na posição 1, ele é pulado: `maior([10, 20])` dá 10 |
| maior_8 | **sim** | com `>=`, em caso de empate `m` recebe um valor igual ao que já tinha, e a função devolve só o valor |
| dia_do_maior_9 | **sim** | começando em 0, compara `temps[0] > temps[0]`, que é sempre falso, então `pos` não muda |
| dia_do_maior_11 | não | se o maior estiver na posição 1, ele é pulado: `dia_do_maior([10, 20])` dá 0 |
| dia_do_maior_12 | não | em empate, `pos` vai para o último dia em vez do primeiro: `dia_do_maior([30, 30])` dá 1 |

**c) Testes novos e MS**

Testes novos: `maior([10, 20]) == 20`, `dia_do_maior([10, 20]) == 1`, `dia_do_maior([30, 30]) == 0`, e a mensagem exata `"lista vazia"` nos dois testes da lista vazia.

| | Gerados | Mortos | Equivalentes | MS |
|---|---|---|---|---|
| Antes | 22 | 11 | 2 | 11/(22 - 2) = 55% |
| Depois | 22 | 20 | 2 | 20/(22 - 2) = 100% |

Sem tirar os equivalentes o mutmut mostra 20 de 22 (91%), porque ele não marca equivalente sozinho.

**d) `>` virar `>=`: equivalente numa função e não na outra**

Em `maior`, a função devolve o valor. Com `>=`, num empate o `m` troca por um valor igual, então o resultado é o mesmo. Em `dia_do_maior`, a função devolve a posição, e a especificação pede o primeiro dia. Com `>=`, num empate o `pos` anda para o dia mais tarde, e a saída muda (`[30, 30]` dá 1 em vez de 0). Ou seja, a equivalência depende do que a função devolve e do que a especificação exige.

---

## Exercício 4 - Parcelamento

**a) Suíte por valor-limite (feita antes de rodar qualquer ferramenta)**

Valor fixo de 1200. Para n, as fronteiras do intervalo [1, 12] pelos seis valores da aula 6 (0, 1, 2, 11, 12, 13), mais a fronteira dos juros em 3 e 4 (último sem juros e primeiro com juros) e o 5.

| n | Classe | Esperado |
|---|---|---|
| 0 | inválido (abaixo do mínimo) | ValueError |
| 1 | mínimo | 1200.0 |
| 2 | acima do mínimo | 600.0 |
| 3 | último sem juros | 400.0 |
| 4 | primeiro com juros | 306.0 |
| 5 | segundo com juros | 249.6 |
| 11 | abaixo do máximo | 126.55 |
| 12 | máximo | 118.0 |
| 13 | inválido (acima do máximo) | ValueError |

**b) Cobertura e MS**

| Cobertura de ramos | Gerados | Mortos | Vivos | MS |
|---|---|---|---|---|
| 100% | 27 | 23 | 4 | 23/27 = 85% |

**c) Análise dos vivos**

| Mutante | Mudança | Resultado |
|---|---|---|
| 6, 7, 8 | mensagem `None`, `"XXparcelas invalidasXX"`, `"PARCELAS INVALIDAS"` | não equivalentes: morrem conferindo a mensagem exata com `str(erro.value)` |
| 9 | `n <= 3` vira `n < 3` | **equivalente**: a única entrada em que a decisão muda é n = 3, e aí o `else` calcula `0.02 * (3 - 3) = 0`, o mesmo que `juros = 0` |

| Cobertura de ramos | Gerados | Mortos | Equivalentes | MS final |
|---|---|---|---|---|
| 100% | 27 | 26 | 1 | 26/(27 - 1) = 100% |

**d) Mutante de segunda ordem (à mão)**

Juntei o mutante 10 (`n <= 3` vira `n <= 4`) com o mutante 17 (`0.02 * (n - 3)` vira `0.02 * (n - 4)`):

```python
if n <= 4:
    juros = 0
else:
    juros = 0.02 * (n - 4)
```

**e) A suíte mata?**

Mata. Rodando a suíte nesse mutante, 4 testes falham (n = 4, 5, 11 e 12). Isso bate com o efeito de acoplamento: defeitos simples e defeitos combinados costumam estar ligados, então uma suíte que mata os mutantes simples tende a matar também os combinados. Offutt (1992) mostrou isso na prática, com testes que matavam os mutantes de primeira ordem matando quase todos os de segunda ordem. Aqui os dois mutantes já eram mortos por conta própria (o 10 morre com n = 4 e o 17 com n a partir de 4), e a combinação não escondeu um do outro.
