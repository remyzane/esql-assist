pip install -r requirements-prd.txt
pip install -r requirements-dev.txt

git clone https://github.com/unimassystem/esql.git
cd esql
git submodule update --init --recursive
