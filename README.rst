Pygov-br é uma lib que tem o objetivo de unificar as API's de dados abertos
governamentais brasileiros. Atualmente, a pygov-br tem suporte para:

* Webservices da Câmara dos Deputados

Instalação
----------

::

    pip install pygov-br

Utilização
----------

::

    from pygov_br.camara_deputados import cd
    cd.deputies.all()

