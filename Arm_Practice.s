.global start
_start:
	mov r0, #0xFF
	mov r1, #22
	and r2, r0,r1
	orr r3, r1,r0
	eor r4, r1,r0
	mvn r5,r0 @Negates r0
	subs r6, r5,#0xffffff00
	mov r6,#0xFF2
	lsl r0,#2
	lsr r0,#2
	mov r9, r6, ror #2
	mov r7,#1