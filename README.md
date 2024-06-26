# affiliate-blog-vue

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## For Ubuntu

```
sudo apt-get update

sudo apt-get upgrade

sudo apt install python3-pip zip
```

## Project Setup

```sh
python3 -m venv env

source env/bin/activate

pip install fastapi uvicorn mangum

pip freeze > requirements.txt
```

requirements.txt will be:

fastapi==0.99.0

mangum==0.17.0

### Compile and Hot-Reload for Development

```sh
pip3 install -t dependencies -r requirements.txt
```

### Compile and Minify for Production

```sh
(cd dependencies; zip ../aws_lambda_artifact.zip -r .)

zip aws_lambda_artifact.zip -u lambda_function.py
```
