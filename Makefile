PKG_NAME := gcc
URL := https://mirrors.kernel.org/gnu/gcc/gcc-8.2.0/gcc-8.2.0.tar.gz

include ../common/Makefile.common

GCCGIT = ~/git/gcc
GCCVER = 8_2_0

GCCTAG = gcc-$(GCCVER)-release
GCCBRANCH = origin/gcc-$(shell echo $(GCCVER) | sed 's/_.*//')-branch

update:
	git -C $(GCCGIT) remote update -p
	git -C $(GCCGIT) shortlog $(GCCTAG)..$(GCCBRANCH) > gcc-stable-branch.patch
	git -C $(GCCGIT) diff $(GCCTAG)..$(GCCBRANCH) >> gcc-stable-branch.patch
	! git diff --exit-code  gcc-stable-branch.patch > /dev/null
	$(MAKE) bumpnogit
	git commit -m "stable branch update" -a
	test -n "$(NO_KOJI)" || $(MAKE) koji-nowait
