# Spotify Downloader


## Tópicos

- [Spotify Downloader](#spotify-downloader)
  - [Tópicos](#tópicos)
  - [Sobre o Projeto](#sobre-o-projeto)
  - [Tecnologias e Ferramentas utilizadas](#tecnologias-e-ferramentas-utilizadas)
  - [Instalação](#instalação)
  - [Execução](#execução)
  - [Licença](#licença)
  - [Contato](#contato)


---
## Sobre o Projeto

Esse projeto visa a criação de uma ferramenta simples para baixar suas músicas em formato .mp3 e manter elas atualizadas com albuns e playlists do Spotify.

O intuito da ferramenta era ser algo simples e que resolvesse um problema que eu enfrentava, que era o seguinte, eu particularmente gosto bastante de ouvir música e, além de ouvir por streaming pelo Spotify, queria ter elas disponíveis em formato .mp3 para conseguir transferir para um pendrive por exemplo e ter acesso a elas em outros dispositivos.

O download das musicas em si não era a tarefa mais difícil na verdade, há bastante ferramentas disponíveis que já fazem o download do Spotify para .mp3, porém a maior dificuldade era para atualizar as playlists, visto que toda vez que eu queria atualizar minhas musicas, precisava ou baixar toda a playlist novamente(o que as vezes podia demorar) ou saber exatamente quais musicas eu já tinha baixado antes e assim fazer o download manualmente só das que realmente eu precisava.

E o objetivo dessa ferramenta é esse, é uma ferramenta de linha de comando para você baixar suas musicas, albuns ou playlists do Spotify, mas que consegue guardar, no caso de albuns e playlists, quais musicas você já baixou, e assim quando for baixar novamente a playlist, fazer o download só das músicas que você ainda não tem, de uma forma facilitada.

---
## Tecnologias e Ferramentas utilizadas

- **Python** -> Linguagem base para a criação da ferramenta;
- **Peewee** -> ORM destinado a criar e gerenciar tabelas de banco de dados relacionais através de objetos Python;
- **SQLite** -> Banco de dados relacional e open source;
- **Paralelismo** -> Utilizado algoritmo de processamento paralelo para otimizar o processo de download das músicas;

---
## Instalação

1. O processo é bem simples, basta copiar o projeto utilizando o comando:

```sh
git clone https://github.com/marcoswb/spotify-downloader.git
```

2. Utilizar o comando a seguir para entrar dentro do projeto:
  
```sh
cd spotify-downloader
```

3. Utilizar o comando a seguir para instalar as dependências Python:
  
```sh
python -m pip install -r requirements.txt
```

Com isso o projeto será criado com todas as dependências devidamente instaladas e linkadas.


---
## Execução

1. Faça login no [console de desenvolvedor do Spotify](https://developer.spotify.com/dashboard/applications) e crie um novo app.

1. Após criar o app, você deve ter acesso as credenciais de CLIENT_ID e CLIENT_SECRET.
   
1. Com essas variáveis em mãos, crie um arquivo **.env** na raíz do projeto e dentro dele informe as seguintes variáveis de ambiente:  
  - `SPOTIFY_CLIENT_ID` -> CLIENT_ID copiado do console do Spotify;
  - `SPOTIFY_CLIENT_SECRET` -> CLIENT_SECRET copiado do console do Spotify;

4. Após isso, é só executar o arquivo **main.py** e utilizar a ferramenta.

---
## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.


---
## Contato

Marcos Warmling Berti - **marcos_wb@outlook.com**
