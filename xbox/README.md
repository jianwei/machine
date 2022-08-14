1.git clone https://github.com/redis/hiredis
    sudo make && make insstall
2.sudo apt-get install -y libhiredis-dev




build:
g++  first.cpp -o first -lhiredis 
g++  first.cpp -o second -lhiredis 