set -e -o pipefail
exit
GCCGIT=~/git/gcc

git -C $GCCGIT remote update
git -C $GCCGIT checkout hj3/users/hjl/x86/gcc-12
git -C $GCCGIT merge --no-edit -s ort -X ours origin/releases/gcc-12
git -C $GCCGIT shortlog --no-merges origin/releases/gcc-11.. > ./gcc-hj-latest.patch
git -C $GCCGIT diff origin/releases/gcc-12.. >> ./gcc-hj-latest.patch
git -C $GCCGIT checkout master

git add gcc-hj-latest.patch
