# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей и системы в целом

# ниже данные представленны следующим образом
# Х гамма из спавочника ; Р_Х ВБР элементов
#                                 шт. Название
t=1
exp=2.71828

R1=0.015
P_R1=exp*(-R1*t)     # 1  Блок (резистор.) Б19К-2-10кОм±10%	ОЖ0.206.018ТУ

V1=0.00103
P_V1=exp*(-V1*t)**2   # 2  Вилка СНП59-64/94х11В-23-1-В	НЩ0.364.061ТУ                8

V2=0.0157
P_V2=exp*(-V2*t)     # 2  Гнездо Г1,6 чер."5" В	ТУ6315.00207593842
                     #  (не нашел гамму в справочнике, взял типовую)	             8
D1=0.17
P_D1=exp*(-D1*t)**2   # 2  Диод 2Д212Б /СО 	АЕЯР.432120.177ТУ                        8

D2=0.078
P_D2=exp*(-D2*t)**2   # 2  Диод 2Д222АС 	аА0.339.327ТУ	                          8

D3=0.032
P_D3=exp*(-D3*t)**2   # 2  Диод 2Д522Б	ДР3.362.029-01ТУ/02	38            8

I1=0.18
P_I1=exp*(-I1*t)     # 1  индикатор ИПД148В-Л	аА0.339.189ТУ                           4

I2=0.21;    P_I2=exp(-R1*t);     # 1  Индикатор ИПВ72А1-4/5х7К (красный)	АЕЯР.432220.232ТУ       4
C1=0.033;   P_C1=exp(-R1*t)^8;   # 8  Конд. К10-17а-М47-22 пФ±10%-В	ОЖ0.460.107ТУ                   32
C2=0.033;   P_C2=exp(-R1*t);     # 2  Конд. К10-17а-М47-330 пФ±10%-В	ОЖ0.460.107ТУ               8
C3=0.033;   P_C3=exp(-R1*t);     # 1  Конд. К10-17а-МП0-50 В-47 пФ±10%-1-В	ОЖ0.460.107ТУ			4
C4=0.033;   P_C4=exp(-R1*t)^30;  # 30 Конд. К10-17а-Н90-0,033 мкФ-В	ОЖ0.460.107ТУ                   120
C5=0.155;   P_C5=exp(-R1*t)^2;   # 2  Конд. К53-18-20В-22 мкФ±10%-В	ОЖ0.464.136ТУ                   8
C6=0.155;   P_C6=exp(-R1*t)^2;   # 2  Конд. К53-18-20В-47 мкФ±10%-В	ОЖ0.464.136ТУ                   8
C7=0.155;   P_C7=exp(-R1*t)^3;   # 3  Конд. К53-18-20В-100 мкФ±10%-В	ОЖ0.464.136ТУ               12
M1=0.0291;  P_M1=exp(-R1*t);     # 1 (взял типовую) Микросборка 852ИН2П	АЕЯР.431230.419ТУ           4
M2=0.0485;  P_M2=exp(-R1*t)^2;   # 2(типовая 386 бит ЗУ)Микросхема 1533АП6*5	бК0.347.364-55ТУ    8
M3=0.0485;  P_M3=exp(-R1*t)^2;   # 2  Микросхема 1533ИД7*5	бК0.347.364-08ТУ                        4
M4=0.0485;  P_M4=exp(-R1*t)^2;   # 2  Микросхема 1533ИР24*5	бКЩ.347.364-38ТУ                        4
M5=0.0485;  P_M5=exp(-R1*t);     # 1  Микросхема 1533КП7*5	бК0.347.364-12ТУ                        4
M6=0.0485;  P_M6=exp(-R1*t)^3;   # 3  Микросхема 1533ЛА3*5	бК0.347.364-01ТУ                        12
M7=0.0485;  P_M7=exp(-R1*t)^2;   # 2  Микросхема 1533ЛЕ1*5	бК0.347.364-05ТУ                        8
M8=0.0485;  P_M8=exp(-R1*t);     # 1  Микросхема 1533ЛИ1*5	бК0.347.364-13ТУ                        4
M9=0.0485;  P_M9=exp(-R1*t);     # 1  Микросхема 1533ЛП3*5	бК0.347.364-15ТУ                        4 (это элемент или в мажоритарном узел)
M10=0.0485; P_M10=exp(-R1*t)^4;  # 4  Микросхема 1533ТМ2*5	бК0.347.364-02ТУ                        16
M11=0.0485; P_M11=exp(-R1*t);    # 1  Микросхема 1533ТМ9*5	бК0.347.364-24ТУ                        4
M12=0.0388; P_M12=exp(-R1*t);    # 1  (взял типовую 78 бит ЗУ)Микросхема 533ЛЕ4	бК0.347.141ТУ46/02  4
M13=0.0388; P_M13=exp(-R1*t);    # 1  Микросхема 533ЛЛ1	бК0.347.141ТУ7/02                           4
M14=0.0388; P_M14=exp(-R1*t)^2;  # 2  Микросхема 533ТЛ2	бК0.347.141ТУ16/02                          8
M15=0.0872; P_M15=exp(-R1*t);    # 1  (типовая 4684 бит ЗУ) Микросхема 588ВГ7 бК0.347.367-12ТУ      4
M16=0.4362; P_M16=exp(-R1*t)^4;  # 4  (типовая для макс. знач. ЗУ) Микросхема РIС17С44-33 I/P(40)   16
R2=0.063;   P_R2=exp(-R1*t)^4;   # 4  Резист. С2-33Н-0,125-100 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ       16
R3=0.063;   P_R3=exp(-R1*t);     # 1  Резист. С2-33Н-0,125-220 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ       4
R4=0.063;   P_R4=exp(-R1*t)^7;   # 7  Резист. С2-33Н-0,125-470 Ом ±5% А-Д-В	ОЖ0.467.093ТУ           28
R5=0.063;   P_R5=exp(-R1*t);     # 1  Резист. С2-33Н-0,125-510 Ом ±5% А-Д-В	ОЖ0.467.093ТУ           4
R6=0.063;   P_R6=exp(-R1*t)^22;  # 22 Резист. С2-33Н-0,125-1 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ           88
R7=0.063;   P_R7=exp(-R1*t)^2;   # 2  Резист. С2-33Н-0,125-22 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ       8
R8=0.063;   P_R8=exp(-R1*t);     # 1  Резист. С2-33Н-0,125-51 кОм ±5% А-Д-В	ОЖ0.467.093ТУ           4
R9=0.063;   P_R9=exp(-R1*t);     # 1  Резист. С2-33Н-0,5-390 Ом±5% А-Д-В 	ОЖ0.467.093ТУ           4
RZ1=0.013;  P_RZ1=exp(-R1*t);    # 1  Резонатор РК386М-4АК-5000 кГц	ТУ6321-004-07614320-96          4
RZ2=0.013;  P_RZ2=exp(-R1*t);    # 1  Резонатор РК386ММ-4АК-12000 К-В	ТУ6321-004-07614320-96      4
RZ3=0.013;  P_RZ3=exp(-R1*t)^4;  # 4  Резонатор РК386ММ-4АК-33000 кГц	ТУ6321-004-07614320-96      16
V3=0.00074; P_V3=exp(-R1*t);     # 1  Розетка РП15-9 ГВФ-В "5"	НКЦС.434410.509ТУ                   4
D4=0.01;    P_D4=exp(-R1*t);     # 1  Стабилитрон 2С147В 	СМ3.362.839ТУ                           4
T1=0.036;   P_T1=exp(-R1*t)^5;   # 5  Транзистор 2Т208А (3л)	ЮФ3.365.035ТУ                       20
TR=0.0019;  P_TR=exp(-R1*t);     # 1  Трансформатор ТИЛ3В "5"	АГ0.472.105ТУ                       4

# P=exp(-m*t)*(3*exp(-2*d*t)-2*exp(-3*d*t)); %

#print(P);
