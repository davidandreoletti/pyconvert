curl -L https://github.com/davidandreoletti/pyconvert/tarball/v0.0.1 2>/dev/null > sources.tar.gz
mkdir pyconvert-0.0.1; tar -C pyconvert-0.0.1 --strip-components 1 -xzvf sources.tar.gz
cd pyconvert-0.0.1
