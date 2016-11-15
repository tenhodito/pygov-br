.. image:: https://travis-ci.org/tenhodito/pygov-br.svg?branch=dev
    :target: https://travis-ci.org/tenhodito/pygov-br
.. image:: https://landscape.io/github/tenhodito/pygov-br/dev/landscape.svg?style=flat
   :target: https://landscape.io/github/tenhodito/pygov-br/dev
   :alt: Code Health
.. image:: https://coveralls.io/repos/github/tenhodito/pygov-br/badge.svg?branch=dev
    :target: https://coveralls.io/github/tenhodito/pygov-br?branch=dev


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

