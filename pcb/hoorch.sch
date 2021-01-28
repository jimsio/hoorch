EESchema Schematic File Version 4
LIBS:hoorch-cache
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
L Connector:Raspberry_Pi_2_3 J2
U 1 1 5D7F4D58
P 5900 3800
F 0 "J2" H 5900 5278 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 5900 5187 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 5900 3800 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 5900 3800 50  0001 C CNN
	1    5900 3800
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male on-off1
U 1 1 5D7F5438
P 9200 3300
F 0 "on-off1" H 9173 3180 50  0000 R CNN
F 1 "Conn_01x02_Male" H 9173 3271 50  0000 R CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 9200 3300 50  0001 C CNN
F 3 "~" H 9200 3300 50  0001 C CNN
	1    9200 3300
	-1   0    0    1   
$EndComp
Wire Wire Line
	9000 3200 7700 3200
Wire Wire Line
	7700 3200 7700 5300
Wire Wire Line
	5500 5300 5500 5200
$Comp
L Connector:Conn_01x02_Male 5V-GND1
U 1 1 5D7F5B1E
P 9300 5550
F 0 "5V-GND1" H 9273 5430 50  0000 R CNN
F 1 "Conn_01x02_Male" H 9273 5521 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 9300 5550 50  0001 C CNN
F 3 "~" H 9300 5550 50  0001 C CNN
	1    9300 5550
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x03_Male amp_L-G-R1
U 1 1 5D7F5D50
P 9300 5150
F 0 "amp_L-G-R1" H 9273 5080 50  0000 R CNN
F 1 "Conn_01x03_Male" H 9273 5171 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 9300 5150 50  0001 C CNN
F 3 "~" H 9300 5150 50  0001 C CNN
	1    9300 5150
	-1   0    0    1   
$EndComp
Text Label 9500 4850 0    50   ~ 0
audio
$Comp
L Connector:Conn_01x02_Male J3
U 1 1 5D7F619D
P 10150 5050
F 0 "J3" H 10256 5228 50  0000 C CNN
F 1 "speaker_L-GND" H 10256 5137 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 10150 5050 50  0001 C CNN
F 3 "~" H 10150 5050 50  0001 C CNN
	1    10150 5050
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J4
U 1 1 5D7F61DD
P 10150 5450
F 0 "J4" H 10256 5628 50  0000 C CNN
F 1 "speaker_R-GND" H 10256 5537 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 10150 5450 50  0001 C CNN
F 3 "~" H 10150 5450 50  0001 C CNN
	1    10150 5450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female speakers1
U 1 1 5D7F664A
P 10900 5300
F 0 "speakers1" H 10927 5276 50  0000 L CNN
F 1 "Conn_01x04_Female" H 10927 5185 50  0000 L CNN
F 2 "Connector_JST:JST_EH_B04B-EH-A_1x04_P2.50mm_Vertical" H 10900 5300 50  0001 C CNN
F 3 "~" H 10900 5300 50  0001 C CNN
	1    10900 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	7950 5450 7950 2100
Wire Wire Line
	7950 5450 9100 5450
Wire Wire Line
	9100 5550 5600 5550
Wire Wire Line
	5600 5550 5600 5200
$Comp
L Device:R R1
U 1 1 5D7F825C
P 3450 3850
F 0 "R1" V 3243 3850 50  0000 C CNN
F 1 "R" V 3334 3850 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 3850 50  0001 C CNN
F 3 "~" H 3450 3850 50  0001 C CNN
	1    3450 3850
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5D7F8D87
P 3450 4050
F 0 "R2" V 3243 4050 50  0000 C CNN
F 1 "R" V 3334 4050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 4050 50  0001 C CNN
F 3 "~" H 3450 4050 50  0001 C CNN
	1    3450 4050
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 5D7F95AF
P 3450 4250
F 0 "R3" V 3243 4250 50  0000 C CNN
F 1 "R" V 3334 4250 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 4250 50  0001 C CNN
F 3 "~" H 3450 4250 50  0001 C CNN
	1    3450 4250
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 5D7F95BD
P 3450 4450
F 0 "R4" V 3243 4450 50  0000 C CNN
F 1 "R" V 3334 4450 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 4450 50  0001 C CNN
F 3 "~" H 3450 4450 50  0001 C CNN
	1    3450 4450
	0    1    1    0   
$EndComp
$Comp
L Device:R R5
U 1 1 5D7F9A13
P 3450 4650
F 0 "R5" V 3243 4650 50  0000 C CNN
F 1 "R" V 3334 4650 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 4650 50  0001 C CNN
F 3 "~" H 3450 4650 50  0001 C CNN
	1    3450 4650
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 5D7F9A21
P 3450 4850
F 0 "R6" V 3243 4850 50  0000 C CNN
F 1 "R" V 3334 4850 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical" V 3380 4850 50  0001 C CNN
F 3 "~" H 3450 4850 50  0001 C CNN
	1    3450 4850
	0    1    1    0   
$EndComp
Wire Wire Line
	2750 3850 2750 3950
Wire Wire Line
	2750 3950 2600 3950
Wire Wire Line
	2750 3850 3300 3850
Wire Wire Line
	2950 4250 2950 4150
Wire Wire Line
	2950 4250 3300 4250
Wire Wire Line
	2900 4250 2900 4450
Wire Wire Line
	2900 4450 3300 4450
Wire Wire Line
	3300 4650 2850 4650
Wire Wire Line
	2850 4350 2850 4650
Wire Wire Line
	2750 4450 2750 4850
Wire Wire Line
	2750 4850 3300 4850
Wire Wire Line
	6700 4000 7050 4000
Wire Wire Line
	7050 4000 7050 5400
Wire Wire Line
	7050 5400 3900 5400
Wire Wire Line
	3900 5400 3900 3850
Wire Wire Line
	3900 3850 3600 3850
Wire Wire Line
	6700 3900 7150 3900
Wire Wire Line
	7150 3900 7150 5500
Wire Wire Line
	7150 5500 4050 5500
Wire Wire Line
	4050 5500 4050 4050
Wire Wire Line
	4050 4050 3600 4050
Wire Wire Line
	6700 4500 7200 4500
Wire Wire Line
	7200 4500 7200 5600
Wire Wire Line
	7200 5600 4100 5600
Wire Wire Line
	4100 5600 4100 4250
Wire Wire Line
	4100 4250 3600 4250
Wire Wire Line
	4450 4650 3600 4650
Wire Wire Line
	5100 3400 4450 3400
Wire Wire Line
	4450 3400 4450 4650
Wire Wire Line
	5100 4100 4550 4100
Wire Wire Line
	4550 4100 4550 4850
Wire Wire Line
	4550 4850 3600 4850
Connection ~ 5500 5300
Wire Wire Line
	5500 5300 1950 5300
Wire Wire Line
	1950 5300 1950 4450
Wire Wire Line
	1950 3950 2100 3950
Connection ~ 1950 4450
Wire Wire Line
	2100 4450 1950 4450
Wire Wire Line
	1950 3950 1950 4050
Connection ~ 1950 4350
Wire Wire Line
	1950 4350 1950 4450
Connection ~ 1950 4250
Wire Wire Line
	1950 4250 1950 4350
Connection ~ 1950 4150
Wire Wire Line
	1950 4150 1950 4250
Connection ~ 1950 4050
Wire Wire Line
	1950 4050 1950 4150
$Comp
L Connector:Conn_01x02_Male volume+1
U 1 1 5D82D0D1
P 8550 2600
F 0 "volume+1" H 8523 2573 50  0000 R CNN
F 1 "Conn_01x02_Male" H 8523 2482 50  0000 R CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 8550 2600 50  0001 C CNN
F 3 "~" H 8550 2600 50  0001 C CNN
	1    8550 2600
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male volume-1
U 1 1 5D82D141
P 8600 2900
F 0 "volume-1" H 8573 2873 50  0000 R CNN
F 1 "Conn_01x02_Male" H 8573 2782 50  0000 R CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 8600 2900 50  0001 C CNN
F 3 "~" H 8600 2900 50  0001 C CNN
	1    8600 2900
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7500 2900 8150 2900
Wire Wire Line
	8350 2600 8150 2600
Wire Wire Line
	8350 2700 8150 2700
Wire Wire Line
	8150 2700 8150 2900
Connection ~ 8150 2900
Wire Wire Line
	8150 2900 8400 2900
$Comp
L Connector:Conn_01x03_Male volume_in1
U 1 1 5D7F69F5
P 8650 5150
F 0 "volume_in1" H 8756 5428 50  0000 C CNN
F 1 "Conn_01x03_Male" H 8756 5337 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 8650 5150 50  0001 C CNN
F 3 "~" H 8650 5150 50  0001 C CNN
	1    8650 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8850 5250 9100 5250
Wire Wire Line
	8850 5050 9100 5050
Wire Wire Line
	9100 5150 8850 5150
$Comp
L Connector:Conn_01x03_Male headphones_2
U 1 1 5D8FB5EE
P 10850 4100
F 0 "headphones_2" H 10823 4123 50  0000 R CNN
F 1 "Conn_01x03_Male" H 10823 4032 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 10850 4100 50  0001 C CNN
F 3 "~" H 10850 4100 50  0001 C CNN
	1    10850 4100
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x05_Male headphones_1
U 1 1 5D9009BD
P 10850 4550
F 0 "headphones_1" H 10823 4573 50  0000 R CNN
F 1 "Conn_01x05_Male" H 10823 4482 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 10850 4550 50  0001 C CNN
F 3 "~" H 10850 4550 50  0001 C CNN
	1    10850 4550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	10350 5150 10400 5150
Wire Wire Line
	10400 5150 10400 4350
Wire Wire Line
	10400 4350 10450 4350
Wire Wire Line
	10300 4750 10300 4200
Wire Wire Line
	10300 4200 10650 4200
Wire Wire Line
	10550 4550 10550 4100
Wire Wire Line
	10550 4100 10650 4100
Wire Wire Line
	10550 4550 10650 4550
Wire Wire Line
	10650 4000 10450 4000
Wire Wire Line
	10450 4000 10450 4350
Connection ~ 10450 4350
Wire Wire Line
	10450 4350 10650 4350
Wire Wire Line
	10550 4550 10550 5450
Wire Wire Line
	10550 5450 10350 5450
Connection ~ 10550 4550
Wire Wire Line
	10350 5050 10450 5050
Wire Wire Line
	10600 5050 10600 5300
Wire Wire Line
	10600 5300 10700 5300
Wire Wire Line
	10600 5300 10600 5400
Wire Wire Line
	10600 5400 10700 5400
Connection ~ 10600 5300
Wire Wire Line
	10600 5400 10600 5550
Wire Wire Line
	10600 5550 10350 5550
Connection ~ 10600 5400
Wire Wire Line
	10450 4750 10450 5050
Wire Wire Line
	10450 4750 10300 4750
Connection ~ 10450 5050
Wire Wire Line
	10450 5050 10600 5050
Wire Wire Line
	10650 4450 10500 4450
Wire Wire Line
	10500 4450 10500 5200
Wire Wire Line
	10500 5200 10700 5200
Wire Wire Line
	10650 5500 10700 5500
$Comp
L Connector:Conn_01x08_Female RFID-1
U 1 1 5D95E83A
P 1900 1200
F 0 "RFID-1" H 1794 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 1794 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 1900 1200 50  0001 C CNN
F 3 "~" H 1900 1200 50  0001 C CNN
	1    1900 1200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2100 900  2350 900 
Wire Wire Line
	2350 900  2350 2000
Wire Wire Line
	2350 2000 3150 2000
Wire Wire Line
	6700 4100 6800 4100
Wire Wire Line
	6800 1950 6050 1950
Wire Wire Line
	2300 1950 2300 1000
Wire Wire Line
	2300 1000 2100 1000
Wire Wire Line
	2100 1100 2250 1100
Wire Wire Line
	2250 1100 2250 1900
Wire Wire Line
	2250 1900 3050 1900
Wire Wire Line
	6750 4200 6700 4200
Wire Wire Line
	5100 4000 4600 4000
Wire Wire Line
	4600 4000 4600 1850
Wire Wire Line
	4600 1850 2400 1850
Wire Wire Line
	2400 1850 2400 1200
Wire Wire Line
	2400 1200 2100 1200
Wire Wire Line
	5700 2500 5700 2100
Wire Wire Line
	5700 2100 5100 2100
Wire Wire Line
	2450 2100 2450 1300
Wire Wire Line
	2450 1300 2100 1300
Wire Wire Line
	4200 1800 3550 1800
Wire Wire Line
	2500 1800 2500 1400
Wire Wire Line
	2500 1400 2100 1400
Connection ~ 5500 5100
Wire Wire Line
	5500 5100 4200 5100
$Comp
L Connector:Conn_01x08_Female RFID-2
U 1 1 5D9A80E9
P 2650 1200
F 0 "RFID-2" H 2544 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 2544 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 2650 1200 50  0001 C CNN
F 3 "~" H 2650 1200 50  0001 C CNN
	1    2650 1200
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female RFID-3
U 1 1 5D9AD8EF
P 3250 1200
F 0 "RFID-3" H 3144 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 3144 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 3250 1200 50  0001 C CNN
F 3 "~" H 3250 1200 50  0001 C CNN
	1    3250 1200
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female RFID-4
U 1 1 5D9B30EF
P 3900 1200
F 0 "RFID-4" H 3794 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 3794 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 3900 1200 50  0001 C CNN
F 3 "~" H 3900 1200 50  0001 C CNN
	1    3900 1200
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female RFID-5
U 1 1 5D9B88F9
P 4700 1200
F 0 "RFID-5" H 4594 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 4594 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 4700 1200 50  0001 C CNN
F 3 "~" H 4700 1200 50  0001 C CNN
	1    4700 1200
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female RFID-6
U 1 1 5D9BE105
P 5450 1200
F 0 "RFID-6" H 5344 1685 50  0000 C CNN
F 1 "Conn_01x08_Female" H 5344 1594 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 5450 1200 50  0001 C CNN
F 3 "~" H 5450 1200 50  0001 C CNN
	1    5450 1200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3150 2000 3150 900 
Wire Wire Line
	3150 900  2850 900 
Connection ~ 3150 2000
Wire Wire Line
	3150 2000 3800 2000
Wire Wire Line
	3450 900  3800 900 
Wire Wire Line
	3800 900  3800 2000
Connection ~ 3800 2000
Wire Wire Line
	3800 2000 4650 2000
Wire Wire Line
	4100 900  4650 900 
Wire Wire Line
	4650 900  4650 2000
Connection ~ 4650 2000
Wire Wire Line
	4650 2000 5400 2000
Wire Wire Line
	4900 900  5400 900 
Wire Wire Line
	5400 900  5400 2000
Connection ~ 5400 2000
Wire Wire Line
	5400 2000 6150 2000
Wire Wire Line
	5650 900  6150 900 
Wire Wire Line
	6150 900  6150 2000
Wire Wire Line
	2850 1000 3100 1000
Wire Wire Line
	3100 1000 3100 1950
Connection ~ 3100 1950
Wire Wire Line
	3100 1950 2300 1950
Wire Wire Line
	3450 1000 3750 1000
Wire Wire Line
	3750 1000 3750 1950
Connection ~ 3750 1950
Wire Wire Line
	3750 1950 3100 1950
Wire Wire Line
	4100 1000 4500 1000
Wire Wire Line
	4500 1000 4500 1950
Connection ~ 4500 1950
Wire Wire Line
	4500 1950 3750 1950
Wire Wire Line
	4900 1000 5300 1000
Wire Wire Line
	5300 1000 5300 1950
Connection ~ 5300 1950
Wire Wire Line
	5300 1950 4500 1950
Wire Wire Line
	5650 1000 6050 1000
Wire Wire Line
	6050 1000 6050 1950
Connection ~ 6050 1950
Wire Wire Line
	6050 1950 5300 1950
Wire Wire Line
	2850 1100 3050 1100
Wire Wire Line
	3050 1100 3050 1900
Connection ~ 3050 1900
Wire Wire Line
	3050 1900 3700 1900
Wire Wire Line
	3450 1100 3700 1100
Wire Wire Line
	3700 1100 3700 1900
Connection ~ 3700 1900
Wire Wire Line
	3700 1900 4450 1900
Wire Wire Line
	4100 1100 4450 1100
Wire Wire Line
	4450 1100 4450 1900
Connection ~ 4450 1900
Wire Wire Line
	4450 1900 5200 1900
Wire Wire Line
	4900 1100 5200 1100
Wire Wire Line
	5200 1100 5200 1900
Connection ~ 5200 1900
Wire Wire Line
	5200 1900 6000 1900
Wire Wire Line
	6000 1100 6000 1900
Connection ~ 6000 1900
Wire Wire Line
	5650 1100 6000 1100
Wire Wire Line
	2850 1300 2950 1300
Wire Wire Line
	2950 1300 2950 2100
Connection ~ 2950 2100
Wire Wire Line
	2950 2100 2450 2100
Wire Wire Line
	3450 1300 3600 1300
Wire Wire Line
	3600 1300 3600 2100
Connection ~ 3600 2100
Wire Wire Line
	3600 2100 2950 2100
Wire Wire Line
	4100 1300 4350 1300
Wire Wire Line
	4350 1300 4350 2100
Connection ~ 4350 2100
Wire Wire Line
	4350 2100 3600 2100
Wire Wire Line
	4900 1300 5100 1300
Wire Wire Line
	5100 1300 5100 2100
Connection ~ 5100 2100
Wire Wire Line
	5100 2100 4350 2100
Wire Wire Line
	5650 1300 5850 1300
Wire Wire Line
	5850 1300 5850 2100
Wire Wire Line
	2850 1400 2900 1400
Wire Wire Line
	2900 1400 2900 1800
Connection ~ 2900 1800
Wire Wire Line
	2900 1800 2500 1800
Wire Wire Line
	4100 1400 4200 1400
Wire Wire Line
	4200 1400 4200 1800
Connection ~ 4200 1800
Wire Wire Line
	4900 1400 5000 1400
Wire Wire Line
	5000 1400 5000 2300
Wire Wire Line
	5000 2300 4200 2300
Connection ~ 4200 2300
Wire Wire Line
	5650 1400 5750 1400
Wire Wire Line
	5750 1400 5750 2300
Wire Wire Line
	5750 2300 5000 2300
Connection ~ 5000 2300
Wire Wire Line
	5100 4200 4100 4200
Wire Wire Line
	4100 4200 4100 2250
Wire Wire Line
	4100 2250 3000 2250
Wire Wire Line
	3000 2250 3000 1200
Wire Wire Line
	3000 1200 2850 1200
Wire Wire Line
	5100 4400 4800 4400
Wire Wire Line
	4800 4400 4800 2550
Wire Wire Line
	4800 2550 4300 2550
Wire Wire Line
	4300 2550 4300 1200
Wire Wire Line
	4300 1200 4100 1200
Wire Wire Line
	4900 1200 5150 1200
Wire Wire Line
	5150 1200 5150 2550
Wire Wire Line
	5150 2550 4900 2550
Wire Wire Line
	4900 2550 4900 4500
Wire Wire Line
	4900 4500 5100 4500
Wire Wire Line
	5650 1200 5950 1200
Wire Wire Line
	5950 1200 5950 2350
Wire Wire Line
	5950 2350 4950 2350
Wire Wire Line
	4950 2350 4950 3800
Wire Wire Line
	4950 3800 5100 3800
Wire Wire Line
	3450 1400 3550 1400
Wire Wire Line
	3550 1400 3550 1800
Connection ~ 3550 1800
Wire Wire Line
	3550 1800 2900 1800
Wire Wire Line
	6000 1900 6750 1900
Wire Wire Line
	5850 2100 7950 2100
Connection ~ 6150 2000
Wire Wire Line
	6150 2000 6950 2000
Wire Wire Line
	6950 4300 6700 4300
Wire Wire Line
	6950 2000 6950 4300
Wire Wire Line
	4200 5100 4200 2400
Wire Wire Line
	4200 2400 4200 2300
Connection ~ 4200 2400
Wire Wire Line
	4200 2400 7150 2400
Wire Wire Line
	6800 1950 6800 4100
Connection ~ 6950 2000
Wire Wire Line
	7550 2000 6950 2000
Wire Wire Line
	6750 1900 6750 4200
$Comp
L Mechanical:MountingHole H1
U 1 1 5DD2726E
P 950 1400
F 0 "H1" H 1050 1446 50  0000 L CNN
F 1 "MountingHole" H 1050 1355 50  0000 L CNN
F 2 "MountingHole:MountingHole_4.3mm_M4" H 950 1400 50  0001 C CNN
F 3 "~" H 950 1400 50  0001 C CNN
	1    950  1400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 5DD283B5
P 950 1700
F 0 "H2" H 1050 1746 50  0000 L CNN
F 1 "MountingHole" H 1050 1655 50  0000 L CNN
F 2 "MountingHole:MountingHole_4.3mm_M4" H 950 1700 50  0001 C CNN
F 3 "~" H 950 1700 50  0001 C CNN
	1    950  1700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 5DD28E3F
P 950 2000
F 0 "H3" H 1050 2046 50  0000 L CNN
F 1 "MountingHole" H 1050 1955 50  0000 L CNN
F 2 "MountingHole:MountingHole_4.3mm_M4" H 950 2000 50  0001 C CNN
F 3 "~" H 950 2000 50  0001 C CNN
	1    950  2000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male led1
U 1 1 5DD48160
P 2400 3350
F 0 "led1" V 2462 3394 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 3394 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 3350 50  0001 C CNN
F 3 "~" H 2400 3350 50  0001 C CNN
	1    2400 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	2600 3950 2600 3550
Wire Wire Line
	2600 3550 2400 3550
Wire Wire Line
	2300 3550 2300 3600
Wire Wire Line
	2300 3600 2100 3600
Wire Wire Line
	2100 3600 2100 3950
$Comp
L Connector:Conn_01x02_Male led2
U 1 1 5DD6D521
P 2400 3650
F 0 "led2" V 2462 3694 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 3694 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 3650 50  0001 C CNN
F 3 "~" H 2400 3650 50  0001 C CNN
	1    2400 3650
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x02_Male led3
U 1 1 5DD6DD47
P 2400 3900
F 0 "led3" V 2462 3944 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 3944 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 3900 50  0001 C CNN
F 3 "~" H 2400 3900 50  0001 C CNN
	1    2400 3900
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x02_Male led4
U 1 1 5DD6E2FF
P 2400 4150
F 0 "led4" V 2462 4194 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 4194 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 4150 50  0001 C CNN
F 3 "~" H 2400 4150 50  0001 C CNN
	1    2400 4150
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x02_Male led5
U 1 1 5DD6E87B
P 2400 4400
F 0 "led5" V 2462 4444 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 4444 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 4400 50  0001 C CNN
F 3 "~" H 2400 4400 50  0001 C CNN
	1    2400 4400
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x02_Male led6
U 1 1 5DD6ED7E
P 2400 4650
F 0 "led6" V 2462 4694 50  0000 L CNN
F 1 "Conn_01x02_Male" V 2553 4694 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Vertical" H 2400 4650 50  0001 C CNN
F 3 "~" H 2400 4650 50  0001 C CNN
	1    2400 4650
	0    1    1    0   
$EndComp
Wire Wire Line
	2200 4050 2200 3850
Wire Wire Line
	2200 3850 2300 3850
Wire Wire Line
	1950 4050 2200 4050
Wire Wire Line
	2200 4150 2200 4100
Wire Wire Line
	2200 4100 2300 4100
Wire Wire Line
	1950 4150 2200 4150
Wire Wire Line
	2300 4350 2200 4350
Wire Wire Line
	2200 4350 2200 4250
Wire Wire Line
	1950 4250 2200 4250
Wire Wire Line
	2150 4350 2150 4450
Wire Wire Line
	2150 4450 2250 4450
Wire Wire Line
	2250 4450 2250 4600
Wire Wire Line
	2250 4600 2300 4600
Wire Wire Line
	1950 4350 2150 4350
Wire Wire Line
	2300 4850 2100 4850
Wire Wire Line
	2100 4850 2100 4450
Wire Wire Line
	2550 4450 2550 4850
Wire Wire Line
	2550 4850 2400 4850
Wire Wire Line
	2550 4450 2750 4450
Wire Wire Line
	2400 4600 2500 4600
Wire Wire Line
	2500 4600 2500 4350
Wire Wire Line
	2500 4350 2850 4350
Wire Wire Line
	2400 4350 2450 4350
Wire Wire Line
	2450 4350 2450 4250
Wire Wire Line
	2450 4250 2900 4250
Wire Wire Line
	2500 4150 2500 4100
Wire Wire Line
	2500 4100 2400 4100
Wire Wire Line
	2500 4150 2950 4150
Wire Wire Line
	2550 4050 2550 3850
Wire Wire Line
	2550 3850 2400 3850
Wire Wire Line
	2550 4050 3300 4050
$Comp
L Mechanical:MountingHole H4mitte1
U 1 1 5D8552D9
P 950 2300
F 0 "H4mitte1" H 1050 2346 50  0000 L CNN
F 1 "MountingHole" H 1050 2255 50  0000 L CNN
F 2 "MountingHole:MountingHole_6.4mm_M6" H 950 2300 50  0001 C CNN
F 3 "~" H 950 2300 50  0001 C CNN
	1    950  2300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole pischrauben1
U 1 1 5D892BB4
P 950 2600
F 0 "pischrauben1" H 1050 2646 50  0000 L CNN
F 1 "MountingHole" H 1050 2555 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 950 2600 50  0001 C CNN
F 3 "~" H 950 2600 50  0001 C CNN
	1    950  2600
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole pischrauben2
U 1 1 5D8AD054
P 950 2900
F 0 "pischrauben2" H 1050 2946 50  0000 L CNN
F 1 "MountingHole" H 1050 2855 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 950 2900 50  0001 C CNN
F 3 "~" H 950 2900 50  0001 C CNN
	1    950  2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	10650 4650 10650 4600
Wire Wire Line
	10650 4600 10950 4600
Wire Wire Line
	10950 4600 10950 5600
Wire Wire Line
	10950 5600 10650 5600
Wire Wire Line
	10650 5600 10650 5500
Wire Wire Line
	10600 5050 10600 4750
Wire Wire Line
	10600 4750 10650 4750
Connection ~ 10600 5050
Wire Wire Line
	5850 2100 5700 2100
Connection ~ 5850 2100
Connection ~ 5700 2100
Wire Wire Line
	5500 5300 6200 5300
Wire Wire Line
	6200 5100 6200 5300
Connection ~ 6200 5300
Wire Wire Line
	5100 3300 3750 3300
Wire Wire Line
	3750 3300 3750 4450
Wire Wire Line
	3750 4450 3600 4450
Wire Wire Line
	4200 2300 4200 1800
Wire Wire Line
	6700 3500 7300 3500
Wire Wire Line
	7300 3500 7300 2200
Wire Wire Line
	7300 2200 3650 2200
Wire Wire Line
	3650 2200 3650 1200
Wire Wire Line
	3650 1200 3450 1200
Wire Wire Line
	9000 3300 8500 3300
Wire Wire Line
	8500 3300 8500 4600
Wire Wire Line
	8500 4600 6700 4600
Wire Wire Line
	7500 2900 7500 5300
Wire Wire Line
	6200 5300 7500 5300
Connection ~ 7500 5300
Wire Wire Line
	7500 5300 7700 5300
Wire Wire Line
	5100 3200 5000 3200
Wire Wire Line
	5000 3200 5000 2450
Wire Wire Line
	5000 2450 8150 2450
Wire Wire Line
	8150 2450 8150 2600
Wire Wire Line
	5100 3700 4350 3700
Wire Wire Line
	4350 3700 4350 2250
Wire Wire Line
	4350 2250 7700 2250
Wire Wire Line
	7700 2250 7700 3000
Wire Wire Line
	7700 3000 8400 3000
Wire Wire Line
	5600 5200 5500 5200
Connection ~ 5500 5200
Wire Wire Line
	5500 5200 5500 5100
$EndSCHEMATC
