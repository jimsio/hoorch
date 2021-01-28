EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Amplifier_Audio:LM386 U1
U 1 1 5DD66421
P 3150 2250
F 0 "U1" H 3494 2296 50  0000 L CNN
F 1 "LM386" H 3494 2205 50  0000 L CNN
F 2 "Package_DIP:DIP-8_W7.62mm" H 3250 2350 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm386.pdf" H 3350 2450 50  0001 C CNN
	1    3150 2250
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5DD66D4A
P 3400 2650
F 0 "R1" V 3193 2650 50  0000 C CNN
F 1 "R" V 3284 2650 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3330 2650 50  0001 C CNN
F 3 "~" H 3400 2650 50  0001 C CNN
	1    3400 2650
	0    1    1    0   
$EndComp
$Comp
L Device:C C3
U 1 1 5DD6779C
P 3550 2450
F 0 "C3" H 3665 2496 50  0000 L CNN
F 1 "C" H 3665 2405 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm" H 3588 2300 50  0001 C CNN
F 3 "~" H 3550 2450 50  0001 C CNN
	1    3550 2450
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C1
U 1 1 5DD67FB8
P 3750 2250
F 0 "C1" V 4005 2250 50  0000 C CNN
F 1 "CP" V 3914 2250 50  0000 C CNN
F 2 "Capacitor_THT:CP_Radial_D10.0mm_P3.80mm" H 3788 2100 50  0001 C CNN
F 3 "~" H 3750 2250 50  0001 C CNN
	1    3750 2250
	0    -1   -1   0   
$EndComp
$Comp
L Device:CP C2
U 1 1 5DD684E8
P 3400 1950
F 0 "C2" V 3655 1950 50  0000 C CNN
F 1 "CP" V 3564 1950 50  0000 C CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 3438 1800 50  0001 C CNN
F 3 "~" H 3400 1950 50  0001 C CNN
	1    3400 1950
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x02_Female J4
U 1 1 5DD69B42
P 4150 2600
F 0 "J4" H 4178 2576 50  0000 L CNN
F 1 "Conn_01x02_Female" H 4178 2485 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 4150 2600 50  0001 C CNN
F 3 "~" H 4150 2600 50  0001 C CNN
	1    4150 2600
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Female J3
U 1 1 5DD6A01D
P 4100 1750
F 0 "J3" H 4128 1726 50  0000 L CNN
F 1 "Conn_01x02_Female" H 4128 1635 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 4100 1750 50  0001 C CNN
F 3 "~" H 4100 1750 50  0001 C CNN
	1    4100 1750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Female J2
U 1 1 5DD6A404
P 2500 2550
F 0 "J2" H 2392 2225 50  0000 C CNN
F 1 "Conn_01x02_Female" H 2392 2316 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 2500 2550 50  0001 C CNN
F 3 "~" H 2500 2550 50  0001 C CNN
	1    2500 2550
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x03_Female J1
U 1 1 5DD6ABE6
P 2450 1750
F 0 "J1" H 2342 1425 50  0000 C CNN
F 1 "Conn_01x03_Female" H 2342 1516 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 2450 1750 50  0001 C CNN
F 3 "~" H 2450 1750 50  0001 C CNN
	1    2450 1750
	-1   0    0    1   
$EndComp
Wire Wire Line
	2700 2550 2800 2550
Wire Wire Line
	2650 1750 2800 1750
Wire Wire Line
	2800 1750 2800 2350
Connection ~ 2800 2550
Wire Wire Line
	2800 2550 2950 2550
Wire Wire Line
	2850 2350 2800 2350
Connection ~ 2800 2350
Wire Wire Line
	2800 2350 2800 2550
Wire Wire Line
	2650 1650 2850 1650
Wire Wire Line
	2850 1650 2850 1850
Wire Wire Line
	2650 1850 2850 1850
Connection ~ 2850 1850
Wire Wire Line
	2850 1850 2850 2150
Wire Wire Line
	3150 1950 3250 1950
Wire Wire Line
	3550 1950 3700 1950
Wire Wire Line
	3700 1950 3700 1750
Wire Wire Line
	3700 1750 3800 1750
Wire Wire Line
	3450 2250 3550 2250
Wire Wire Line
	3900 1850 3900 2250
Wire Wire Line
	3950 2600 3950 2250
Wire Wire Line
	3950 2250 3900 2250
Connection ~ 3900 2250
Wire Wire Line
	3550 2600 3550 2650
Wire Wire Line
	3550 2300 3550 2250
Connection ~ 3550 2250
Wire Wire Line
	3550 2250 3600 2250
Wire Wire Line
	3250 2650 3100 2650
Wire Wire Line
	2950 2650 2950 2550
Wire Wire Line
	3950 2700 3650 2700
Wire Wire Line
	3100 2700 3100 2650
Connection ~ 3100 2650
Wire Wire Line
	3800 1750 3800 1450
Wire Wire Line
	3800 1450 5300 1450
Wire Wire Line
	5300 1450 5300 2900
Wire Wire Line
	5300 2900 3650 2900
Wire Wire Line
	3650 2900 3650 2700
Connection ~ 3800 1750
Wire Wire Line
	3800 1750 3900 1750
Connection ~ 3650 2700
Wire Wire Line
	3650 2700 3100 2700
Wire Wire Line
	3050 1950 3050 1900
Wire Wire Line
	3050 1900 2750 1900
Wire Wire Line
	2750 1900 2750 2450
Wire Wire Line
	2750 2450 2700 2450
Wire Wire Line
	2950 2650 3050 2650
Wire Wire Line
	3050 2550 3050 2650
Connection ~ 3050 2650
Wire Wire Line
	3050 2650 3100 2650
$EndSCHEMATC
