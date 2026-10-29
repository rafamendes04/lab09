import pytest
from parcelamento import parcela


@pytest.mark.parametrize("n", [0, 13])
def test_parcelas_invalidas(n):
    with pytest.raises(ValueError) as erro:
        parcela(1200, n)
    assert str(erro.value) == "parcelas invalidas"


@pytest.mark.parametrize("n, esperado", [
    (1, 1200.0),
    (2, 600.0),
    (3, 400.0),
    (4, 306.0),
    (5, 249.6),
    (11, 126.55),
    (12, 118.0),
], ids=["min", "acima_min", "limite_sem_juros", "primeira_com_juros", "segunda_com_juros", "abaixo_max", "max"])
def test_valor_da_parcela(n, esperado):
    assert parcela(1200, n) == esperado
