PKG_NAME := gcc
URL := https://mirrors.kernel.org/gnu/gcc/gcc-8.2.0/gcc-8.2.0.tar.gz

include ../common/Makefile.common

GCCGIT = ~/git/gcc
GCCVER = 8_2_0

update:
	git -C $(GCCGIT) remote update -p
	git -C $(GCCGIT) shortlog gcc-8_2_0-release..origin/gcc-8-branch > gcc-stable-branch.patch
	git -C $(GCCGIT) diff gcc-8_2_0-release..origin/gcc-8-branch >> gcc-stable-branch.patch
	! git diff --exit-code  gcc-stable-branch.patch > /dev/null
	git commit -m "stable branch update" gcc-stable-branch.patch
	$(MAKE) bump
	test -n "$(NO_KOJI)" || $(MAKE) koji-nowait
