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
	git -C $(GCCGIT) diff $(GCCTAG)..$(GCCBRANCH) -- \* ':!*/DATESTAMP' >> gcc-stable-branch.patch
	git -C $(GCCGIT) show $(GCCBRANCH):gcc/DATESTAMP > DATESTAMP
	git -C $(GCCGIT) cat-file -p $(GCCBRANCH) | sed -En '/^git-svn-id:.*\/branches\/(.*) .*/s//\1/p' > REVISION
	! git diff --exit-code  gcc-stable-branch.patch > /dev/null
	$(MAKE) bumpnogit
	git commit -m "stable update to `cat REVISION`" -a
	test -n "$(NO_KOJI)" || $(MAKE) koji-nowait
