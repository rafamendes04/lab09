from carrinho import total_com_desconto


def test_total():
    assert total_com_desconto([10, 20, 30, 40, 50]) == 141


def test_preco_com_centavos():
    assert total_com_desconto([10, 20, 30, 10.55]) == 69.5
