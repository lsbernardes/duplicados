duplicados.py
========

Descrição
--------

**duplicados.py** é um script Python que usa __hashs md5sum__ para identificar arquivos duplicados dentro de uma pasta, ainda que eles tenham nomes completamente diferentes. Criei esse script porque tenho muitos livros escaneados e às vezes, sem querer, acabo baixando arquivos que eu já tenho. Claro que o script vale para qualquer formato de arquivo.

O script foi feito pra distribuições Linux, pois usa comandos Linux como o `mdsum`, por isso não sei se é possível adaptá-lo ao Windows, mas suponho que é possível, sobretudo agora que a Microsoft tem integrado o Linux ao seu sistema.

Embora o script seja funcional, apresente os resultados da busca sem problemas, há ainda algumas coisas que eu preciso afinar e ajustar, portanto, em certo sentido ele ainda está em desenvolvimento.

Dependências
--------

Só há uma dependência necessária para executar **duplicados.py**, que é o `tqdm`
Usando `pip` é fácil instalá-lo com esse comando::

    pip install tqdm

Uso
--------

**duplicados.py** precisa ser utilizado dentro do shell (interpretador) Python. O que ele faz não é mais do que criar um objeto sobre o qual é possível aplicar alguns métodos. Aqui vai um passo do seu uso:

Primeiro, é preciso executar o arquivo dentro do shell::

	In [1]: run duplicados.py

Uma vez executado, é preciso criar um objeto e indicar o rota da pasta a ser pesquisada::

	In [1]: pasta = duplicados('/media/data/texto/artigos')
	Gerando o JSON...
	100%|█████████████████████████████████████████████████████████| 2061/2061 [00:59<00:00, 28.72it/s]
	65 arquivos duplicados
	Arquivo GERADO /media/data/texto/artigos/artigos.json


Se é a primeira vez que a pasta é pesquisada, o script vai gerar um arquivo JSON na raiz da pasta contendo as hashs md5sum e os arquivos associados a elas, no seguinte formato::

	{
		'defa1b8ab48bfc3f09d30ca0743cca02': 
			['/media/data/texto/artigos/economia/GEORGESCU-ROEGEN Nicholas. Myths about Energy and Matter.pdf'],
		'5f1dd4dd561f2dd2ece55e3fc3621c13': 
			['/media/data/texto/artigos/economia/Resenha FURTADO Celso. O mito do desenvolvimento economico.pdf'],
		'bcf0c3271be3211ef7d2ad093c558d89': 
			['/media/data/texto/artigos/A virada neoliberal do governo Dilma.pdf'],
		'42af77c0bb346a42f9d93ebdc6d3fa0d': 
			['/media/data/texto/artigos/sociologia/CRITICAS A SOCIEDAD DE MERCADO 50 Aniversario de la muerte de Karl Polanyi.pdf'],
		'2d780cdda527814c92320375f2a8ee45': 
			['/media/data/texto/artigos/NovosEstudos/67/20080625 reflexoes sobre a historia.pdf',
			'/media/data/texto/artigos/NovosEstudos/69/20080625 reflexoes sobre a historia.pdf'],
		...
	}

Uma vez gerado o arquivo, mesmo que se execute o script mais uma vez o arquivo não será atualizado pelos próximos 7 dias. É possível mudar esse parâmetro alterando a variável `DIAS` no começo do script de acordo com o intervalo desejado, `0` é o intervalo de quem quer que o arquivo seja atualizado sempre que o script for executado.

Duas variáveis de objetos contém informações que podem interessar: o objeto `pasta` criado acima terá a variável de objeto `pasta.DIC` que contém um dictionário com as hashs e os arquivos a elas associados e o objeto `pasta.DUPL` contendo as hashs dos arquivos duplicados nessa pasta. Para ver a lista dos arquivos duplicados basta executar o método de classe `pasta.duplicados()`. Assim serão apresentados os arquivos duplicados, enumerados e coloridos. O primeiro arquivo em amarelo e os outros com a cor padrão do sistema::

	 1   (2)
	/media/data/texto/artigos/sociologia/SINGER André. Raízes sociais e ideológicas do Lulismo.pdf
	/media/data/texto/artigos/NovosEstudos/143/20091215 06 singer p82a103.pdf
	 2   (2)
	/media/data/texto/artigos/sociologia/REIS Wanderley. Política e participação.pdf
	/media/data/texto/artigos/sociologia/Fábio Wanderley REIS. Política e participação. Notas sobre aspectos doutrinários e empíricos.pdf
	 3   (2)
	/media/data/texto/artigos/sociologia/Livros que Inventaram o Brasil.pdf
	/media/data/texto/artigos/NovosEstudos/71/20080625 livros que inventaram.pdf
	 4   (2)
	/media/data/texto/artigos/sociologia/entrevistas/Lembrar Bourdieu. Entrevistas.pdf
	/media/data/texto/artigos/NovosEstudos/96/20080627 lembrar bourdieu.pdf
	 5   (3)
	/media/data/texto/artigos/filosofia/ STROUD Stroud. The Significance of Naturalized Epistemology.pdf
	/media/data/texto/artigos/filosofia/STROUD Barry. The Significance of Naturalized Epistemology.pdf
	/media/data/texto/artigos/filosofia/STROUD Stroud. The Significance of Naturalized Epistemology.pdf
	 6   (7)
	/media/data/texto/artigos/NovosEstudos/88/20080627 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/65/20080624 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/59/20080623 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/60/20080624 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/63/20080624 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/76/20080626 poemas.pdf
	/media/data/texto/artigos/NovosEstudos/64/20080624 poemas.pdf

	...

Há ainda um método que permite buscar duplicados a partir de dois objetos já criados, mas esse método ainda está em desenvolvimento. Queria também criar um método que apagasse os arquivos duplicados, claro, sempre pedindo a confirmação do usuário. Logo, quem sabe esses métodos estarão disponíveis :)
