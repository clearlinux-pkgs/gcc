pushd ~/git/gcc
git remote update
git checkout hj3/users/hjl/x86/gcc-11
git merge --no-edit origin/releases/gcc-11
git shortlog origin/releases/gcc-11.. > ~/clear/packages/gcc/gcc-hj-latest.patch
git diff origin/releases/gcc-11.. >> ~/clear/packages/gcc/gcc-hj-latest.patch
git checkout master
popd
git add gcc-hj-latest.patch

