include /usr/local/etc/PcapPlusPlus.mk

all:
	g++ $(PCAPPP_INCLUDES) --std=c++17 -c -o main.o main.cpp
	g++ $(PCAPPP_LIBS_DIR) --std=c++17 -static-libstdc++ -o main.exe main.o $(PCAPPP_LIBS)

clean:
	rm main.o
	rm main.exe