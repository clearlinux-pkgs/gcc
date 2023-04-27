#!/bin/bash
set -e -o pipefail

if ! test `find "timestamp" -mmin +10000`
then
    echo "not old enough"
#    exit
fi
touch timestamp

#bash hj.sh

export GCCGIT=~/git/gcc
export GCCVER=13.1.0

GCCTAG=releases/gcc-"${GCCVER}"
GCCBRANCH=origin/releases/gcc-"$(echo "$GCCVER" | sed 's/\..*//')"

git -C "$GCCGIT" remote update -p
git -C "$GCCGIT" rev-parse --verify --quiet refs/tags/"${GCCTAG}" > /dev/null
git -C "$GCCGIT" rev-parse --verify --quiet "$GCCBRANCH" > /dev/null
git -C "$GCCGIT" diff "${GCCTAG}".."${GCCBRANCH}" -- \* ':!*/DATESTAMP' > new.patch~
git show HEAD:gcc-stable-branch.patch | sed -n '/^diff --git/,$p' > current.patch~
diff current.patch~ new.patch~ > /dev/null && rm current.patch~ new.patch~ && exit
git -C "$GCCGIT" shortlog "${GCCTAG}".."${GCCBRANCH}" > gcc-stable-branch.patch
cat new.patch~ >> gcc-stable-branch.patch
rm -f *.patch~
git -C "$GCCGIT" show "${GCCBRANCH}":gcc/DATESTAMP > DATESTAMP
git -C "$GCCGIT" describe --abbrev=10 --match 'releases/*' "$GCCBRANCH" > REVISION
make bumpnogit
git commit -m "stable update to `cat REVISION`" -a
make koji-nowait
