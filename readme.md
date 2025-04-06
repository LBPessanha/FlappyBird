[![Codacy Badge](https://app.codacy.com/project/badge/Grade/47f911bfe6f54451a6ef3926e5cc9c3d)](https://app.codacy.com/gh/92username/FlappyBird/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Flappy Bird Clone

Este é um clone simples do jogo Flappy Bird, desenvolvido em Python utilizando a biblioteca `pygame`. O objetivo do jogo é controlar o pássaro para que ele passe pelos tubos sem colidir.

## Ambiente Virtual

Recomenda-se usar um ambiente virtual para isolar as dependências deste projeto. Siga as instruções abaixo para criar e ativar um ambiente virtual:

### No Windows

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate
```

### No macOS e Linux

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

Depois de ativar o ambiente virtual, você verá o nome `(venv)` no início da linha de comando, indicando que o ambiente está ativo. Em seguida, instale as dependências conforme mencionado abaixo.

Para desativar o ambiente virtual quando terminar de usar o projeto, simplesmente digite:

```bash
deactivate
```
## Requisitos

Certifique-se de ter o Python instalado em sua máquina. Além disso, instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Como Jogar

1. Execute o programa com o comando:
   ```bash
   python flappyBird.py
   ```
2. Pressione a barra de espaço (`SPACE`) para fazer o pássaro pular.
3. Evite colidir com os tubos ou o chão.
4. A pontuação aumenta a cada tubo que você ultrapassa.

## Estrutura do Projeto

- **`flappyBird.py`**: Arquivo principal contendo toda a lógica do jogo.
- **`requirements.txt`**: Lista de dependências necessárias para executar o jogo.
- **`.gitignore`**: Arquivo para ignorar diretórios e arquivos desnecessários no controle de versão.

## Recursos do Jogo

- **Pássaro animado**: O pássaro bate as asas enquanto voa.
- **Tubo dinâmico**: Os tubos aparecem em posições aleatórias.
- **Chão em movimento**: O chão se move continuamente para simular o deslocamento.
- **Pontuação**: A pontuação é exibida no canto superior direito da tela.

## Imagens

Certifique-se de que as imagens necessárias para o jogo estão localizadas no diretório correto. O código utiliza os seguintes arquivos de imagem:

- `pipe.png`: Imagem do tubo.
- `base.png`: Imagem do chão.
- `bg.png`: Imagem de fundo.
- `bird1.png`, `bird2.png`, `bird3.png`: Imagens para a animação do pássaro.

Atualize os caminhos das imagens no código, se necessário.

## Reinício do Jogo

Se o pássaro colidir com um tubo ou o chão, o jogo será reiniciado automaticamente.

## Licença

Este projeto é apenas para fins educacionais e não possui uma licença específica.

---
Divirta-se jogando!
