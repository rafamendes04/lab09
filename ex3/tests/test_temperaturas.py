import pytest
from temperaturas import maior, dia_do_maior


def test_maior_lista_normal():
    assert maior([21, 25, 19, 30, 22]) == 30


def test_maior_um_elemento():
    assert maior([18]) == 18


def test_maior_primeiro():
    assert maior([30, 21]) == 30


def test_maior_segundo():
    assert maior([10, 20]) == 20


def test_maior_vazia():
    with pytest.raises(ValueError) as erro:
        maior([])
    assert str(erro.value) == "lista vazia"


def test_dia_lista_normal():
    assert dia_do_maior([21, 25, 19, 30, 22]) == 3


def test_dia_um_elemento():
    assert dia_do_maior([18]) == 0


def test_dia_primeiro():
    assert dia_do_maior([30, 21]) == 0


def test_dia_segundo():
    assert dia_do_maior([10, 20]) == 1


def test_dia_empate():
    assert dia_do_maior([30, 30]) == 0


def test_dia_vazia():
    with pytest.raises(ValueError) as erro:
        dia_do_maior([])
    assert str(erro.value) == "lista vazia"
