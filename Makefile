PKG_NAME := gcc
URL := https://mirrors.kernel.org/gnu/gcc/gcc-7.3.0/gcc-7.3.0.tar.gz

include ../common/Makefile.common

GCCVER = 8_2_0

update:
	pushd ~/git/gcc ; git remote update -p ; git diff gcc-8_2_0-release..origin/gcc-8-branch  > ~/clear/packages/gcc/gcc-stable-branch.patch ; popd
	git diff --exit-code  gcc-stable-branch.patch || bash ./update.sh