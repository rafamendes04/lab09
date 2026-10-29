import pytest
from classificacao import classificar_aluno


def test_aprovado():
    assert classificar_aluno(8.0, 80) == "Aprovado"


def test_reprovado():
    assert classificar_aluno(3.0, 90) == "Reprovado"


@pytest.mark.parametrize("media", [-0.1, 10.1])
def test_media_invalida(media):
    with pytest.raises(ValueError) as erro:
        classificar_aluno(media, 80)
    assert str(erro.value) == "Media invalida"


@pytest.mark.parametrize("presenca", [-1, 101])
def test_presenca_invalida(presenca):
    with pytest.raises(ValueError) as erro:
        classificar_aluno(8.0, presenca)
    assert str(erro.value) == "Presenca invalida"


@pytest.mark.parametrize("media, presenca, esperado", [
    (0, 80, "Reprovado"),
    (10, 80, "Aprovado"),
    (8.0, 0, "Reprovado por falta"),
    (8.0, 100, "Aprovado"),
    (8.0, 74, "Reprovado por falta"),
    (8.0, 75, "Aprovado"),
    (7.0, 80, "Aprovado"),
    (6.9, 80, "Recuperacao"),
    (5.0, 80, "Recuperacao"),
    (4.9, 80, "Reprovado"),
])
def test_limites(media, presenca, esperado):
    assert classificar_aluno(media, presenca) == esperado
