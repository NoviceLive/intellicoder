TSTDIR = tests
BINDIR = bin
PIC = write


default:
	make --silent _test CFLAGS="-m64"
	make --silent _test CFLAGS="-m32"


_test:
	mkdir -p ${BINDIR}
	for one in 3; do \
		gcc -g ${CFLAGS} -I. ${TSTDIR}/syscall$${one}-test.c \
			-o ${BINDIR}/syscall$${one}-test && \
		file ${BINDIR}/syscall$${one}-test && \
		${BINDIR}/syscall$${one}-test; \
		sleep 1; \
	done


cpp:
	cpp -m64 -DCPP syscall.c > 64.txt
	cpp -m32 -DCPP syscall.c > 32.txt


write:
	gcc -O2 -I. pic/pic.c pic/syscall.c -o ${BINDIR}/${PIC} && \
		file ${BINDIR}/${PIC} \
		&& objdump -d ${BINDIR}/${PIC} -j .pic -j .pid \
		&& mkhex ${BINDIR}/${PIC} -l -j .pic > 64.c
