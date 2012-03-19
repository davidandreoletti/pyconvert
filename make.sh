# Original idea:
# http://www.voidspace.org.uk/python/weblog/arch_d7_2008_12_06.shtml#e1038

# Variables
PYTHON_APP_NAME="pyconvert-app"
PYTHON_APP_NAME_ZIP="$PYTHON_APP_NAME".zip
PYTHON_APP_NAME_ZIP_DIR="./../$PYTHON_APP_NAME_ZIP"

# Generate stub archive
touch __main__.py
echo "import main" >> __main__.py
#echo "import pdb; pdb.set_trace()" >> __main__.py
echo "main.main()" >> __main__.py

zip "$PYTHON_APP_NAME_ZIP_DIR" __main__.py
zip "$PYTHON_APP_NAME_ZIP_DIR" main.py

touch hashbang.txt
echo "#! /usr/bin/env python" >> hashbang.txt

cat hashbang.txt "$PYTHON_APP_NAME_ZIP_DIR" > "$PYTHON_APP_NAME"
chmod +x "$PYTHON_APP_NAME"

rm -f hashbang.txt
rm -f __main__.py
rm -f "$PYTHON_APP_NAME_ZIP"

echo "DONE"
echo "=============================================================================="
echo "Run application with: ./$PYTHON_APP_NAME -h"
echo "=============================================================================="