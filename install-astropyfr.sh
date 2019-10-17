#pip install -U -r requirements.txt 
cd home
rm -rf astropyfr
git clone https://github.com/stephaneworkspace/astro_py.git astropyfr
cd astropyfr
rm -rf *.*
cd ..
mv astropyfr/astropyfr ..
rm -rf astropyfr
cd ..
rm -rf assets
# Repository private for text on french, this library is not required, text comming from book, not my texts
git clone https://github.com/stephaneworkspace/astro_py_text.git assets