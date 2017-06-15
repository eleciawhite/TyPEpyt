# A simple makefile for building MeArm_Cal_Jetson, a mishmash of Arduino and C++

CC=gcc
CFLAGS=-I.

DEPS = meArm. ik.h configuration.h CommandLine.h MeArm_Calibration.h
OBJ = CommandLine.o ik.o MeArm_Calibration.o meArm.o main.o

%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	$(CC) -o cal $^ $(CFLAGS) 
