#! /bin/sh

if [ -d "env/" ]; then
  echo "environment file already installed"
else
  python3 -m venv env
fi

source env/bin/activate

pip install -r requirements.txt

echo "=---------------------------="
echo "--- installation finished ---"
echo "=---------------------------="

echo "assuming all is well, you can now update token.txt with your discord bot token and run aqutie with:"
echo "source env/bin/activate; python bot.py"
