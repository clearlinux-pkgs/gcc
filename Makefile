PKG_NAME := gcc
URL := https://mirrors.kernel.org/gnu/gcc/gcc-9.1.0/gcc-9.1.0.tar.gz

include ../common/Makefile.common

GCCGIT = ~/git/gcc
GCCVER = 9.2.0

GCCTAG = releases/gcc-$(GCCVER)
GCCBRANCH = origin/releases/gcc-$(shell echo $(GCCVER) | sed 's/\..*//')

update:
	git -C $(GCCGIT) remote update -p
	git -C $(GCCGIT) shortlog $(GCCTAG)..$(GCCBRANCH) > gcc-stable-branch.patch
	git -C $(GCCGIT) diff $(GCCTAG)..$(GCCBRANCH) -- \* ':!*/DATESTAMP' >> gcc-stable-branch.patch
	git -C $(GCCGIT) show $(GCCBRANCH):gcc/DATESTAMP > DATESTAMP
	git -C $(GCCGIT) describe --abbrev=10 $(GCCBRANCH) > REVISION
	! git diff --exit-code  gcc-stable-branch.patch > /dev/null
	$(MAKE) bumpnogit
	git commit -m "stable update to `cat REVISION`" -a
	test -n "$(NO_KOJI)" || $(MAKE) koji-nowait
