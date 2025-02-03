mov R1,2
xor R2,R2
main:
	and R1,1
	je even
	jmp main

even:
	mov R2,1
