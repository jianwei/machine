prepare:
1.git clone https://github.com/redis/hiredis
    sudo make && sudo make install
2.sudo apt-get install -y libhiredis-dev

build:
g++  first.cpp -o second -lhiredis   && ./second




sudo apt-get install libhiredis-dev 