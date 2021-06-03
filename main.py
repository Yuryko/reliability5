# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей и системы в целом

# Значение гаммы взято из спавочника
#                 шт. Название
R1 = 0.015        # 1  Блок (резистор.) Б19К-2-10кОм±10%	ОЖ0.206.018ТУ
V1 = 0.00103      # 2  Вилка СНП59-64/94х11В-23-1-В	НЩ0.364.061ТУ
V2 = 0.0157       # 2  Гнездо Г1,6 чер."5" В	ТУ6315.00207593842  (не нашел гамму в справочнике, взял типовую)
D1 = 0.17         # 2  Диод 2Д212Б /СО 	АЕЯР.432120.177ТУ
D2 = 0.078        # 2  Диод 2Д222АС 	аА0.339.327ТУ
D3 = 0.032        # 2  Диод 2Д522Б	ДР3.362.029-01ТУ/02	38
I1 = 0.18         # 1  индикатор ИПД148В-Л	аА0.339.189ТУ
I2 = 0.21         # 1  Индикатор ИПВ72А1-4/5х7К (красный)	АЕЯР.432220.232ТУ
C1 = 0.033        # 8  Конд. К10-17а-М47-22 пФ±10%-В	ОЖ0.460.107ТУ
C2 = 0.033        # 2  Конд. К10-17а-М47-330 пФ±10%-В	ОЖ0.460.107ТУ
C3 = 0.033        # 1  Конд. К10-17а-МП0-50 В-47 пФ±10%-1-В	ОЖ0.460.107ТУ
C4 = 0.033        # 30 Конд. К10-17а-Н90-0,033 мкФ-В	ОЖ0.460.107ТУ
C5 = 0.155        # 2  Конд. К53-18-20В-22 мкФ±10%-В	ОЖ0.464.136ТУ
C6 = 0.155        # 2  Конд. К53-18-20В-47 мкФ±10%-В	ОЖ0.464.136ТУ
C7 = 0.155        # 3  Конд. К53-18-20В-100 мкФ±10%-В	ОЖ0.464.136ТУ
M1 = 0.0291       # 1 (взял типовую) Микросборка 852ИН2П	АЕЯР.431230.419ТУ
M2 = 0.0485       # 2(типовая 386 бит ЗУ)Микросхема 1533АП6*5	бК0.347.364-55ТУ
M3 = 0.0485       # 2  Микросхема 1533ИД7*5	бК0.347.364-08ТУ
M4 = 0.0485       # 2  Микросхема 1533ИР24*5	бКЩ.347.364-38ТУ
M5 = 0.0485       # 1  Микросхема 1533КП7*5	бК0.347.364-12ТУ
M6 = 0.0485       # 3  Микросхема 1533ЛА3*5	бК0.347.364-01ТУ
M7 = 0.0485       # 2  Микросхема 1533ЛЕ1*5	бК0.347.364-05ТУ
M8 = 0.0485       # 1  Микросхема 1533ЛИ1*5	бК0.347.364-13ТУ
M9 = 0.0485       # 1  Микросхема 1533ЛП3*5	бК0.347.364-15ТУ
M10 = 0.0485      # 1  Микросхема 1533ТМ9*5	бК0.347.364-24ТУ
M11 = 0.0485      # 4  Микросхема 1533ТМ2*5	бК0.347.364-02ТУ
M12 = 0.0388      # 1  (взял типовую 78 бит ЗУ)Микросхема 533ЛЕ4	бК0.347.141ТУ46/02
M13 = 0.0388      # 1  Микросхема 533ЛЛ1	бК0.347.141ТУ7/02
M14 = 0.0388      # 2  Микросхема 533ТЛ2	бК0.347.141ТУ16/02
M15 = 0.0872      # 1  (типовая 4684 бит ЗУ) Микросхема 588ВГ7 бК0.347.367-12ТУ
M16 = 0.4362      # 4  (типовая для макс. знач. ЗУ) Микросхема РIС17С44-33 I/P(40)
R2 = 0.063        # 4  Резист. С2-33Н-0,125-100 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ
R3 = 0.063        # 1  Резист. С2-33Н-0,125-220 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ
R4 = 0.063        # 7  Резист. С2-33Н-0,125-470 Ом ±5% А-Д-В	ОЖ0.467.093ТУ
R5 = 0.063        # 1  Резист. С2-33Н-0,125-510 Ом ±5% А-Д-В	ОЖ0.467.093ТУ
R6 = 0.06         # 22 Резист. С2-33Н-0,125-1 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ
R7 = 0.063        # 2  Резист. С2-33Н-0,125-22 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ
R8 = 0.063        # 1  Резист. С2-33Н-0,125-51 кОм ±5% А-Д-В	ОЖ0.467.093ТУ
R9 = 0.063        # 1  Резист. С2-33Н-0,5-390 Ом±5% А-Д-В 	ОЖ0.467.093ТУ
RZ1 = 0.013       # 1  Резонатор РК386М-4АК-5000 кГц	ТУ6321-004-07614320-96
RZ2 = 0.013       # 1  Резонатор РК386ММ-4АК-12000 К-В	ТУ6321-004-07614320-96
RZ3 = 0.013       # 4  Резонатор РК386ММ-4АК-33000 кГц	ТУ6321-004-07614320-96
V3 = 0.00074      # 1  Розетка РП15-9 ГВФ-В "5"	НКЦС.434410.509ТУ
D4 = 0.01         # 1  Стабилитрон 2С147В 	СМ3.362.839ТУ
T1 = 0.036        # 5  Транзистор 2Т208А (3л)	ЮФ3.365.035ТУ
TR = 0.0019       # 1  Трансформатор ТИЛ3В "5"	АГ0.472.105ТУ

t = 1
exp = 2.71828

P_R1 = exp*(-R1*t)
P_V1 = exp*(-V1*t)**2
P_V2 = exp*(-V2*t)**2
P_D1 = exp*(-D1*t)**2
P_D2 = exp*(-D2*t)**2
P_D3 = exp*(-D3*t)**2
P_I1 = exp*(-I1*t)
P_I2 = exp*(-I2*t)
P_C1 = exp*(-C1*t)**8
P_C2 = exp*(-C2*t)
P_C3 = exp*(-C3*t)
P_C4 = exp*(-C4*t)**30
P_C5 = exp*(-C5*t)**2
P_C6 = exp*(-C6*t)**2
P_C7 = exp*(-C7*t)**3
P_M1 = exp*(-M1*t)
P_M2 = exp*(-M2*t)**2
P_M3 = exp*(-M3*t)**2
P_M4 = exp*(-M4*t)**2
P_M5 = exp*(-M5*t)
P_M6 = exp*(-M6*t)**3
P_M7 = exp*(-M7*t)**2
P_M8 = exp*(-M8*t)
P_M9 = exp*(-M9*t)     # (это элемент или в мажоритарном узел)
P_M10 = exp*(-M10*t)**4
P_M11 = exp*(-M11*t)
P_M12 = exp*(-M12*t)
P_M13 = exp*(-M13*t)
P_M14 = exp*(-M14*t)**2
P_M15 = exp*(-M15*t)
P_M16 = exp*(-M16*t)**4
P_R2 = exp*(-R2*t)**4
P_R3 = exp*(-R3*t)
P_R4 = exp*(-R4*t)**7
P_R5 = exp*(-R5*t)
P_R6 = exp*(-R6*t)**22
P_R7 = exp*(-R7*t)**2
P_R8 = exp*(-R8*t)
P_R9 = exp*(-R9*t)
P_RZ1 = exp*(-RZ1*t)
P_RZ2 = exp*(-RZ2*t)
P_RZ3 = exp*(-RZ3*t)**4
P_V3 = exp*(-V3*t)
P_D4 = exp*(-D4*t)
P_T1 = exp*(-T1*t)   # 5 шт
P_TR = exp*(-TR*t)


mshv = [P_R1, P_V1, P_V2, P_D1, P_D2, P_D3, P_I1, P_I2, P_C1, P_C2, P_C3, P_C4, P_C5, P_C6, P_C7,
               P_M1, P_M2, P_M3, P_M4, P_M5, P_M6, P_M7, P_M8, P_M10, P_M11, P_M12, P_M13, P_M14, P_M15,
               P_M16, P_R2, P_R3, P_R4, P_R5, P_R6, P_R7, P_R8, P_R9, P_RZ1, P_RZ2, P_RZ3, P_V3, P_D4,
               P_T1, P_T1, P_T1, P_T1,P_T1, P_TR]

# P=exp(-m*t)*(3*exp(-2*d*t)-2*exp(-3*d*t)) %

#print(P)
