10 PMODE 4,1:SCREEN 1,1:PCLS 5:COLOR 0,5
20 FOR I = 1 TO 1000
30 X=X+L*SIN(R):Y=Y+L*COS(R)
40 IF X<-128 OR X>128 THEN 90
50 IF Y<-96 OR Y>95 THEN 90
60 LINE -(X+128,Y+96),PSET
70 R1=R1+60:R=R1/57.29578:L=L+0.5
80 NEXT I
90 GOTO 90