%define keepstatic 1
%define gcc_target x86_64-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.28
%define isl_version 0.24
%define gccver 15
%define gccpath gcc-15.1.0
# Highest optimisation ABI we target
%define mtune sapphirerapids

# Lowest compatible ABI (must be lowest of current targets & OBS builders)
# avoton (silvermont target) && ivybridge (OBS builders) = westmere
%define march westmere


%define __strip /bin/true
%define debug_package %{nil}


Name     : gcc
Version  : 15.1.0
Release  : 1950
URL      : http://www.gnu.org/software/gcc/
Source0  : https://gcc.gnu.org/pub/gcc/releases/gcc-15.1.0/gcc-15.1.0.tar.xz 
Source1  : https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.24.tar.bz2
Source2  : DATESTAMP
Source3  : REVISION
Summary  : GNU cc and gcc C compilers
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT


Patch0   : gcc-stable-branch.patch
Patch1   : 0001-Fix-stack-protection-issues.patch
Patch2   : openmp-vectorize-v2.patch
Patch3   : fortran-vector-v2.patch
Patch5   : optimize.patch
Patch6   : vectorize.patch
Patch9   : gomp-relax.patch
Patch11  : memcpy-avx2.patch
Patch14  : arch-native-override.patch
Patch15  : 0001-Ignore-Werror-if-GCC_IGNORE_WERROR-environment-varia.patch
Patch16  : 0001-Always-use-z-now-when-linking-with-pie.patch
Patch19  : tune-inline.patch
Patch20  : vectorcost.patch
Patch22  : compilespeed.patch
Patch23  : spr-default-tuning.patch
Patch24  : 0001-Enforce-debug-level-when-CLEAR_DEBUG_TERSE-is-set.patch
Patch25  : adaptive-mutex.patch
Patch30  : gcc-hj-latest.patch

Patch31  : avx512move.patch


# partial upstream backport
# cves: 1xx


BuildRequires : bison
BuildRequires : flex
BuildRequires : gmp-dev
BuildRequires : libstdc++
BuildRequires : libunwind-dev
BuildRequires : mpc-dev
BuildRequires : mpfr-dev
BuildRequires : pkgconfig(zlib)
BuildRequires : zstd-dev
BuildRequires : sed
BuildRequires : texinfo
BuildRequires : dejagnu
BuildRequires : expect
BuildRequires : autogen
BuildRequires : guile
BuildRequires : tcl
BuildRequires : valgrind-dev
BuildRequires : libxml2-dev
BuildRequires : libxslt
BuildRequires : graphviz
BuildRequires : gdb-dev
BuildRequires : procps-ng
BuildRequires : glibc-libc32
BuildRequires : glibc-dev32
BuildRequires : docbook-xml docbook-utils doxygen
BuildRequires : util-linux


Requires: gcc-libubsan = %{version}-%{release}
Requires: gcc-doc = %{version}-%{release}
Requires: glibc-dev

Provides:       gcc-symlinks
Provides:       cpp
Provides:       cpp-symlinks
Provides:       gcov
Provides:       gfortran-symlinks
Provides:       g77
Provides:       g77-symlinks
Provides:       g++-symlinks
Provides:       g++
Provides:       gfortran
Provides:	gcc15 gcc15-dev
Obsoletes:	gcc14
%description
GNU cc and gcc C compilers.

%package -n gcc-dev
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libgcov-dev
Provides:       libssp-dev
Provides:       libgomp-dev
Provides:       libgcc-s-dev
Provides:       gcc-plugin-dev
Provides:       libstdc++-dev
Requires:       gcc-libs-math = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}
Requires:       gcc-jit = %{version}-%{release}
Requires:       gcc = %{version}-%{release}
Requires:	gcc-libgfortran = %{version}-%{release}

%description -n gcc-dev
GNU cc and gcc C compilers dev files

%package staticdev
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libssp-staticdev
Provides:       libgomp-staticdev
Requires:       gcc-dev

%description staticdev
GNU cc and gcc C compilers dev files (static)





%package dev32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Requires:	gcc-libgcc32

%description dev32
GNU cc and gcc C compilers dev files




%package -n libgcc1
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Requires:       filesystem
Provides:       libssp0
Provides:       libgomp1

%description -n libgcc1
GNU cc and gcc C compilers.

%package libgfortran
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libgfortran
GNU cc and gcc C compilers.

%package libgcc32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libgcc32
GNU cc and gcc C compilers.

%package libubsan
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libubsan
Address sanitizer runtime libs

%package -n libstdc++
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description -n libstdc++
GNU cc and gcc C compilers.

%package  jit
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description jit
GNU cc and gcc C compilers.


%package libstdc++32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libstdc++32
GNU cc and gcc C compilers.

%package -n gcc-doc
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          doc

%package go
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO compiler
Group:          devel

%description go
GNU Compile Collection GO compiler

%package go-lib
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO runtime
Group:          devel

%description go-lib
GNU Compile Collection GO runtime

%description -n gcc-doc
GNU cc and gcc C compilers.

%package locale
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description locale
GNU cc and gcc C compilers.

%package libs-math
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description libs-math
GNU cc and gcc C compilers.


%prep
%setup -q -n %{gccpath}
%patch0 -p1

#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch9 -p1

%patch14 -p1

%patch15 -p1
%patch16 -p1
%patch19 -p1
#%patch20 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1

#%patch30 -p1




%build

# Live in the gcc source tree
tar xf %{SOURCE1} && ln -sf isl-%{isl_version} isl

# Update the DATESTAMP and add a revision
tee `find -name DATESTAMP` > /dev/null < %{SOURCE2}
cp %{SOURCE3} gcc/

rm -rf ../gcc-build
mkdir ../gcc-build
pushd ../gcc-build
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=westmere -g1 -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000 -mtune=sapphirerapids  -fPIC -falign-functions=32  -gz=zstd -gno-column-info -gno-variable-location-views "
export CXXFLAGS="-march=westmere -g1 -O3  -Wl,-z,max-page-size=0x1000 -mtune=sapphirerapids  -fPIC  -gz=zstd -gno-column-info -gno-variable-location-views "
export CFLAGS_FOR_TARGET="$CFLAGS"
export CXXFLAGS_FOR_TARGET="$CXXFLAGS"
export FFLAGS_FOR_TARGET="$FFLAGS"

export CPATH=/usr/include
export LIBRARY_PATH=/usr/lib64

../%{gccpath}/configure \
    --prefix=/usr \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --enable-multilib\
    --enable-lto --with-pic \
    --disable-werror \
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-host-shared \
    --enable-languages="c,c++,fortran,go,jit" \
    --enable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --includedir=/usr/include \
    --exec-prefix=/usr \
    --with-glibc-version=2.35 \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=sapphirerapids \
    --with-arch=westmere \
    --enable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only \
    --enable-linux-futex \
    --enable-gnu-indirect-function \
    --enable-default-pie

make -O %{?_smp_mflags} bootstrap

popd

rm -rf ../gcc-build-avx2
mkdir ../gcc-build-avx2
pushd ../gcc-build-avx2
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=ivybridge -g -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000  -gz=zstd -gno-column-info -gno-variable-location-views "
export CXXFLAGS="-march=ivybridge -g -O3  -Wl,-z,max-page-size=0x1000  -gz=zstd -gno-column-info -gno-variable-location-views "
export CFLAGS_FOR_TARGET="$CFLAGS -march=haswell -mtune=sapphirerapids  -fno-semantic-interposition "
export CXXFLAGS_FOR_TARGET="$CXXFLAGS -march=haswell -mtune=sapphirerapids  -fno-semantic-interposition "
export FFLAGS_FOR_TARGET="$FFLAGS -march=haswell -mtune=sapphirerapids  -fno-semantic-interposition "

export CPATH=/usr/include
export LIBRARY_PATH=%{_libdir}
../%{gccpath}/configure \
    --prefix=/usr \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared \
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --enable-multilib\
    --enable-lto --with-pic\
    --disable-werror \
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-host-shared \
    --enable-languages="c,c++,fortran,go,jit" \
    --enable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --includedir=/usr/include \
    --exec-prefix=/usr \
    --with-glibc-version=2.35 \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=sapphirerapids \
    --with-arch=x86-64-v3 \
    --enable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only \
    --enable-linux-futex \
    --enable-gnu-indirect-function \
    --with-zstd \
    --enable-default-pie

make -O %{?_smp_mflags} profiledbootstrap

popd

rm -rf ../gcc-build-avx512
mkdir ../gcc-build-avx512
pushd ../gcc-build-avx512
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=ivybridge -g -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000  -gz=zstd -gno-column-info -gno-variable-location-views "
export CXXFLAGS="-march=ivybridge -g -O3  -Wl,-z,max-page-size=0x1000  -gz=zstd -gno-column-info -gno-variable-location-views "
export CFLAGS_FOR_TARGET="$CFLAGS -march=x86-64-v4 -mtune=sapphirerapids -fno-semantic-interposition "
export CXXFLAGS_FOR_TARGET="$CXXFLAGS -march=x86-64-v4 -mtune=sapphirerapids -fno-semantic-interposition "
export FFLAGS_FOR_TARGET="$FFLAGS -march=x86-64-v4 -mtune=sapphirerapids -fno-semantic-interposition "

export CPATH=/usr/include
export LIBRARY_PATH=%{_libdir}

../%{gccpath}/configure \
    --prefix=/usr \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --enable-multilib\
    --enable-lto --with-pic\
    --disable-werror \
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-host-shared \
    --enable-languages="c,c++,fortran,go,jit" \
    --enable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --includedir=/usr/include \
    --exec-prefix=/usr \
    --with-glibc-version=2.35 \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=sapphirerapids \
    --with-arch=x86-64-v3 \
    --enable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only \
    --enable-linux-futex \
    --enable-gnu-indirect-function \
    --with-zstd \
    --enable-default-pie

make -O %{?_smp_mflags} profiledbootstrap

popd


# Work around libstdc++'s use of weak symbols to libpthread in static
# mode: libpthread doesn't get pulled in and therefore we get crashes
# due to the calls being resolved to address 0x0.
# We rebuild the .a without weak symbols.
# See:
#  https://sourceware.org/bugzilla/show_bug.cgi?id=5784
#  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78017
#  (and more)
for dir in ../gcc-build/x86_64-generic-linux/{,32}; do
    for lib in libstdc++-v3/libsupc++ libstdc++-v3/src; do
        pushd $dir/$lib
        # Save any shared libraries
        mv .libs saved.libs || :
        rename lib savedlib lib*.so.* || :

        make clean
        make -O %{?_smp_mflags} CPPFLAGS="-D_GLIBCXX_GTHREAD_USE_WEAK=0" \
             LIBGCC2_DEBUG_CFLAGS="-g -DGTHREAD_USE_WEAK=0"

        # Restore the saved shared libraries (if any)
        rename savedlib lib savedlib* || :
        if [ -d saved.libs ]; then
            mv saved.libs/*.so.* .libs || :
        fi

        # Update timestamps so make install won't recreate
        find -name '*.so*' | xargs -rt touch -r `find -name '*.a' | head -1`
        popd
    done
done



%check
pushd ../gcc-build
export CHECK_TEST_FRAMEWORK=1
#make -O -k %{?_smp_mflags} check  || :
popd


%install
export CPATH=/usr/include
export LIBRARY_PATH=/usr/lib64

pushd ../gcc-build-avx512
%make_install_v4
popd
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/lib64/gcc/
rm -rf %{buildroot}/usr/lib64/*.a
rm -rf %{buildroot}/usr/lib64/*.o
rm -rf %{buildroot}/usr/lib64/*.so
rm -rf %{buildroot}/usr/lib64/*.spec

pushd ../gcc-build-avx2
%make_install_v3
popd
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/lib64/gcc/
rm -rf %{buildroot}/usr/lib64/*.a
rm -rf %{buildroot}/usr/lib64/*.o
rm -rf %{buildroot}/usr/lib64/*.so
rm -rf %{buildroot}/usr/lib64/*.spec

pushd ../gcc-build
%make_install
cd -

mkdir -p %{buildroot}-v3/usr/libexec/gccgo/bin
rm -f %{buildroot}-v3/usr/bin/go 
rm -f %{buildroot}-v3/usr/bin/gofmt
mkdir -p %{buildroot}-v4/usr/libexec/gccgo/bin
rm -f %{buildroot}-v4/usr/bin/go 
rm -f %{buildroot}-v4/usr/bin/gofmt


cd %{buildroot}-v3/usr/bin
if [ -e %{gcc_target}-g77 ]; then
    ln -sf %{gcc_target}-g77 g77 || true
    ln -sf g77 f77 || true
fi
if [ -e x86_64-generic-linux-gfortran ]; then
    ln -sf %{gcc_target}-gfortran gfortran || true
    ln -sf gfortran f95 || true
fi
ln -sf %{gcc_target}-g++ g++
ln -sf %{gcc_target}-gcc gcc
#ln -sf %{gcc_target}-cpp cpp
install -d %{buildroot}-v3/usr/lib
ln -sf ../bin/cpp %{buildroot}-v3/usr/lib/cpp
ln -sf g++ c++
ln -sf gcc cc
cd -


cd %{buildroot}-v4/usr/bin
if [ -e %{gcc_target}-g77 ]; then
    ln -sf %{gcc_target}-g77 g77 || true
    ln -sf g77 f77 || true
fi
if [ -e x86_64-generic-linux-gfortran ]; then
    ln -sf %{gcc_target}-gfortran gfortran || true
    ln -sf gfortran f95 || true
fi
ln -sf %{gcc_target}-g++ g++
ln -sf %{gcc_target}-gcc gcc
#ln -sf %{gcc_target}-cpp cpp
install -d %{buildroot}-v4/usr/lib
ln -sf ../bin/cpp %{buildroot}-v4/usr/lib/cpp
ln -sf g++ c++
ln -sf gcc cc
cd -


cd %{buildroot}/usr/bin
if [ -e %{gcc_target}-g77 ]; then
    ln -sf %{gcc_target}-g77 g77 || true
    ln -sf g77 f77 || true
fi
if [ -e x86_64-generic-linux-gfortran ]; then
    ln -sf %{gcc_target}-gfortran gfortran || true
    ln -sf gfortran f95 || true
fi
ln -sf %{gcc_target}-g++ g++
ln -sf %{gcc_target}-gcc gcc
#ln -sf %{gcc_target}-cpp cpp
install -d %{buildroot}/usr/lib
ln -sf ../bin/cpp %{buildroot}/usr/lib/cpp
ln -sf g++ c++
ln -sf gcc cc
cd -



# This conflicts with golang, stash away
# We use gccgo to build golang
mkdir -p %{buildroot}/usr/libexec/gccgo/bin
mv %{buildroot}/usr/bin/go %{buildroot}/usr/libexec/gccgo/bin
mv %{buildroot}/usr/bin/gofmt %{buildroot}/usr/libexec/gccgo/bin

find %{buildroot}/usr/ -name libiberty.a | xargs rm -f
find %{buildroot}/usr/ -name libiberty.h | xargs rm -f
chmod 0755 %{buildroot}*/usr/lib64/libgcc_s.so.1
chmod 0755 %{buildroot}*/usr/lib32/libgcc_s.so.1

chmod a+x %{buildroot}*/usr/bin
chmod a+x %{buildroot}*/usr/lib64
find %{buildroot}*/usr/lib64 %{buildroot}/usr/lib*/gcc -name '*.so*' -print0 | xargs -r0 chmod -f 755
find %{buildroot}*/usr/lib64 %{buildroot}/usr/lib*/gcc -name '*.o' -print0 | xargs -r0 chmod -f 644


# This is only for gdb
mkdir -p %{buildroot}/usr/share/gdb/auto-load/usr/lib64
mkdir -p %{buildroot}/usr/share/gdb/auto-load/usr/lib32
mv %{buildroot}/usr/lib64/libstdc++.so.*-gdb.py %{buildroot}/usr/share/gdb/auto-load/usr/lib64/.
mv %{buildroot}/usr/lib32/libstdc++.so.*-gdb.py %{buildroot}/usr/share/gdb/auto-load/usr/lib32/.

# merge the two C++ include trees (needed for Clang)
pushd %{buildroot}/usr/include/c++/*/x86_64-generic-linux
find -type f \! -path ./32/\* | while read f; do
    cmp -s $f 32/$f && continue
    (
        echo '#ifdef __LP64__'
        cat $f
        echo '#else'
        cat 32/$f
        echo '#endif'
    ) > rpm-tmp-hdr
    mv rpm-tmp-hdr $f
done
for f in ./32/*; do
  rm -rf $f
  ln -s ../$(basename $f) $f
done
popd

# Also clang compat
(cd %{buildroot}/usr/lib64 && ln -s -t . gcc/x86_64-generic-linux/*/*.[ao])
(cd %{buildroot}/usr/lib32 && ln -s -t . ../lib64/gcc/x86_64-generic-linux/*/32/*.[ao])

%find_lang cpplib cpp.lang
%find_lang gcc tmp.lang
%find_lang libstdc++ cxx.lang
cat *.lang > gcc.lang

# we don't want the 32 bit stuff in avx* builds
rm -rf %{buildroot}-v3/usr/lib32
rm -rf %{buildroot}-v4/usr/lib32

# These were moved after elf-move so need to be specially deleted
rm -f %{buildroot}-v3/usr/lib64/libstdc++.so.*-gdb.py
rm -f %{buildroot}-v4/usr/lib64/libstdc++.so.*-gdb.py

rm -f %{buildroot}/usr/lib64/gcc/x86_64-generic-linux/*/include-fixed/pthread.h 

/usr/bin/elf-move.py avx2 %{buildroot}-v3 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name} --skip --path /usr/lib64/gcc/x86_64-generic-linux/%{gccver}/plugin/include/configargs.h
/usr/bin/elf-move.py avx512 %{buildroot}-v4 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name} --skip --path /usr/lib64/gcc/x86_64-generic-linux/%{gccver}/plugin/include/configargs.h

/usr/bin/elf-move.py avx2 %{buildroot}-v3 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name}
/usr/bin/elf-move.py avx512 %{buildroot}-v4 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name}

# we don't want per subarch .a files
rm -f %{buildroot}-v*/usr/lib64/*.a

%files
/usr/bin/%{gcc_target}-gcc-ar
/usr/bin/%{gcc_target}-gcc-ranlib
/usr/bin/%{gcc_target}-gcc-nm
/usr/bin/%{gcc_target}-gcc
/usr/bin/%{gcc_target}-c++
/usr/bin/%{gcc_target}-gcc-%{gccver}
/usr/bin/gcc
/usr/bin/cc
/usr/bin/gcc-ar
/usr/bin/gcc-nm
/usr/bin/gcc-ranlib
/usr/bin/gcov
/usr/bin/gcov-tool
/usr/lib/cpp
/usr/bin/cpp
/usr/bin/lto-dump
#/usr/lib64/libvtv*
/usr/lib64/libcc1*
/usr/lib64/gcc/%{gcc_target}/%{gccver}/include-fixed/
/usr/lib64/gcc/%{gcc_target}/%{gccver}/install-tools/
/usr/lib64/gcc/%{gcc_target}/%{gccver}/libcaf_*
/usr/lib64/gcc/%{gcc_target}/%{gccver}/include/
/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto1
/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto-wrapper
/usr/lib64/gcc/%{gcc_target}/%{gccver}/collect2
/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1plus
/usr/lib64/gcc/%{gcc_target}/%{gccver}/g++-mapper-server
/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gtype.state
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so.*
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/include/
/usr/share/gcc-%{gccver}
/usr/lib64/*.o

#avx2
/V3/usr/lib64/libcc1*

#avx512
/V4/usr/lib64/libcc1*
/V3/usr/bin/cpp
/V4/usr/bin/cpp

# libgcc-s-dev
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbegin.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginS.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginT.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtend.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtendS.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtfastmath.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec32.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec64.o
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec80.o

#gfortran
/usr/bin/%{gcc_target}-gfortran
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/f951
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/finclude
/usr/bin/f95
/usr/bin/gfortran

#g++
/usr/bin/%{gcc_target}-g++
/usr/bin/c++
/usr/bin/g++

# gcc-dev
/usr/lib64/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/liblto_plugin.so




/V3/usr/bin/%{gcc_target}-gcc-ar
/V3/usr/bin/%{gcc_target}-gcc-ranlib
/V3/usr/bin/%{gcc_target}-gcc-nm
/V3/usr/bin/%{gcc_target}-gcc
/V3/usr/bin/%{gcc_target}-c++
/V3/usr/bin/%{gcc_target}-gcc-%{gccver}
/V3/usr/bin/gcc-ar
/V3/usr/bin/gcc-nm
/V3/usr/bin/gcc-ranlib
/V3/usr/bin/gcov
/V3/usr/bin/gcov-tool
/V3/usr/bin/lto-dump
#/usr/lib64/libvtv*
/V3/usr/lib64/libcc1*
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/install-tools/
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto1
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto-wrapper
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/collect2
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1plus
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/g++-mapper-server
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so.*
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/include/
/V3/usr/lib64/*.o

#avx2
/V3/usr/lib64/libcc1*

#avx512
/V4/usr/lib64/libcc1*

# libgcc-s-dev
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbegin.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginS.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginT.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtend.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtendS.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtfastmath.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec32.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec64.o
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec80.o

#gfortran
/V3/usr/bin/%{gcc_target}-gfortran
/V3/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/f951

#g++
/V3/usr/bin/%{gcc_target}-g++

# gcc-dev

/V4/usr/bin/%{gcc_target}-gcc-ar
/V4/usr/bin/%{gcc_target}-gcc-ranlib
/V4/usr/bin/%{gcc_target}-gcc-nm
/V4/usr/bin/%{gcc_target}-gcc
/V4/usr/bin/%{gcc_target}-c++
/V4/usr/bin/%{gcc_target}-gcc-%{gccver}
/V4/usr/bin/gcc-ar
/V4/usr/bin/gcc-nm
/V4/usr/bin/gcc-ranlib
/V4/usr/bin/gcov
/V4/usr/bin/gcov-tool
/V4/usr/bin/lto-dump
#/usr/lib64/libvtv*
/V4/usr/lib64/libcc1*
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/install-tools/
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto1
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/lto-wrapper
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/collect2
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1plus
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/g++-mapper-server
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so.*
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/include/
/V4/usr/lib64/*.o

#avx2
/V3/usr/lib64/libcc1*

#avx512
/V4/usr/lib64/libcc1*

# libgcc-s-dev
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbegin.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginS.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtbeginT.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtend.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtendS.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtfastmath.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec32.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec64.o
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/crtprec80.o

#gfortran
/V4/usr/bin/%{gcc_target}-gfortran
/V4/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/f951

#g++
/V4/usr/bin/%{gcc_target}-g++

# gcc-dev
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so



%files dev
/usr/lib64/libgcc_s.so
/usr/lib64/gcc/%{gcc_target}/%{gccver}/include/ssp
/usr/lib64/libgomp.spec
/usr/lib64/libgfortran.so
/usr/lib64/libgfortran.spec
/usr/include/libgccjit++.h
/usr/include/libgccjit.h
# gcc-plugin-dev
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gengtype
/V3/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gengtype
/V4/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gengtype

# libstdc++
/usr/lib64/libstdc++.so
/usr/include/c++/*
/usr/share/gdb/auto-load/usr/lib64/libstdc++.so.*
/usr/bin/gcov-dump
/V3/usr/bin/gcov-dump
/V4/usr/bin/gcov-dump
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/32/finclude/
/usr/lib64/libatomic.so
/usr/lib64/libitm.so
/usr/lib64/libitm.spec
/usr/lib64/libquadmath.so

#avx2

#avx512


# some basic static files
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/libgcc.a
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/libgcc_eh.a
/usr/lib64/gcc/x86_64-generic-linux/%{gccver}/libgcov.a
/usr/lib64/libgcov.a

%files staticdev
/usr/lib64/*.a

%files dev32
/usr/lib32/crtbegin.o
/usr/lib32/crtbeginS.o
/usr/lib32/crtbeginT.o
/usr/lib32/crtend.o
/usr/lib32/crtendS.o
/usr/lib32/crtfastmath.o
/usr/lib32/crtprec32.o
/usr/lib32/crtprec64.o
/usr/lib32/crtprec80.o
/usr/lib32/libcaf_single.a
/usr/lib32/libgcc.a
/usr/lib32/libgcc_eh.a
/usr/lib32/libgcov.a
/usr/lib32/libstdc++.a
/usr/lib32/libstdc++.so
/usr/lib32/libstdc++fs.a
/usr/lib32/libsupc++.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbegin.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginS.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginT.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtend.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtendS.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtfastmath.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec32.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec64.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec80.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbegin.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginS.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginT.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtend.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtendS.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtfastmath.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec32.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec64.o
/V3/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec80.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbegin.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginS.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtbeginT.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtend.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtendS.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtfastmath.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec32.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec64.o
/V4/usr/lib64/gcc/x86_64-generic-linux/*/32/crtprec80.o
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_arithmetic.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_exceptions.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_features.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/libcaf_single.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcc.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcc_eh.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcov.a
/usr/lib32/libasan.a
/usr/lib32/libasan.so
/usr/lib32/libatomic.a
/usr/lib32/libatomic.so
/usr/lib32/libgfortran.a
/usr/lib32/libgfortran.so
/usr/lib32/libgfortran.spec
/usr/lib32/libgomp.a
/usr/lib32/libgomp.so
/usr/lib32/libgomp.spec
/usr/lib32/libitm.a
/usr/lib32/libitm.so
/usr/lib32/libitm.spec
/usr/lib32/libquadmath.a
/usr/lib32/libquadmath.so
/usr/lib32/libsanitizer.spec
/usr/lib32/libssp.a
/usr/lib32/libssp.so
/usr/lib32/libubsan.a
/usr/lib32/libubsan.so
/usr/lib32/libstdc++exp.a
#/usr/lib64/gcc/x86_64-generic-linux/*/32/include/ISO_Fortran_binding.h

#/usr/lib/libvtv.a
#/usr/lib/libvtv.so
/usr/share/gdb/auto-load/usr/lib32/libstdc++.so.*



%files -n libgcc1
/usr/lib64/libgcc_s.so.1

#avx2
/V3/usr/lib64/libgcc_s.so.1

#avx512
/V4/usr/lib64/libgcc_s.so.1

%files libs-math
/usr/lib64/libssp.so*
/usr/lib64/libgomp*so*
/usr/lib64/libatomic*.so.*
/usr/lib64/libitm*.so.*
/usr/lib64/libquadmath*.so.*

#avx2
/V3/usr/lib64/libssp.so*
/V3/usr/lib64/libgomp*so*
/V3/usr/lib64/libatomic*.so.*
/V3/usr/lib64/libitm*.so.*
/V3/usr/lib64/libquadmath*.so.*

#avx512
/V4/usr/lib64/libssp.so*
/V4/usr/lib64/libgomp*so*
/V4/usr/lib64/libatomic*.so.*
/V4/usr/lib64/libitm*.so.*
/V4/usr/lib64/libquadmath*.so.*

%files libgfortran
/usr/lib64/libgfortran*.so.*
/V3/usr/lib64/libgfortran*.so.*
/V4/usr/lib64/libgfortran*.so.*

%files libgcc32
/usr/lib32/libasan*
/usr/lib32/libatomic.so.1
/usr/lib32/libatomic.so.1.2.0
#/usr/lib32/libcilkrts.so.5
#/usr/lib32/libcilkrts.so.5.0.0
#/usr/lib32/libcilkrts.spec
/usr/lib32/libgcc_s.so
/usr/lib32/libgcc_s.so.1
/usr/lib32/libgfortran.so.5
/usr/lib32/libgfortran.so.5.0.0
%exclude /usr/lib32/libgo.*
%exclude /usr/lib32/libgobegin.a
%exclude /usr/lib32/libgolibbegin.a
/usr/lib32/libgomp.so.1
/usr/lib32/libgomp.so.1.0.0
/usr/lib32/libitm.so.1
/usr/lib32/libitm.so.1.0.0
/usr/lib32/libquadmath.so.0
/usr/lib32/libquadmath.so.0.0.0
/usr/lib32/libssp.so.0
/usr/lib32/libssp.so.0.0.0
/usr/lib32/libssp_nonshared.a
/usr/lib32/libubsan.so.1
/usr/lib32/libubsan.so.1.0.0

%files -n libstdc++
/usr/lib64/libstdc++.so.*
/usr/lib32/libstdc++.modules.json
/usr/lib64/libstdc++.modules.json

#avx2
/V3/usr/lib64/libstdc++.so.*

#avx512
/V4/usr/lib64/libstdc++.so.*

%files jit
/usr/lib64/libgccjit.so
/usr/lib64/libgccjit.so.0
/usr/lib64/libgccjit.so.0.0.1

#avx2
/V3/usr/lib64/libgccjit.so.0.0.1

#avx512
/V4/usr/lib64/libgccjit.so.0.0.1

%files libstdc++32
/usr/lib32/libstdc++.so.*


%files -n gcc-doc
%{_mandir}/man1
%{_mandir}/man7
%{_infodir}

%files go
/usr/libexec/gccgo/bin/*
/usr/bin/gccgo
/usr/bin/x86_64-generic-linux-gccgo
/V3/usr/bin/gccgo
/V3/usr/bin/x86_64-generic-linux-gccgo
/V4/usr/bin/gccgo
/V4/usr/bin/x86_64-generic-linux-gccgo
/usr/lib64/gcc/x86_64-generic-linux/*/cgo
/usr/lib64/gcc/x86_64-generic-linux/*/go1
/usr/lib64/gcc/x86_64-generic-linux/*/buildid
/V3/usr/lib64/gcc/x86_64-generic-linux/*/cgo
/V3/usr/lib64/gcc/x86_64-generic-linux/*/go1
/V3/usr/lib64/gcc/x86_64-generic-linux/*/buildid
/V4/usr/lib64/gcc/x86_64-generic-linux/*/cgo
/V4/usr/lib64/gcc/x86_64-generic-linux/*/go1
/V4/usr/lib64/gcc/x86_64-generic-linux/*/buildid
/usr/lib64/gcc/x86_64-generic-linux/*/test2json
/usr/lib64/gcc/x86_64-generic-linux/*/vet
/V3/usr/lib64/gcc/x86_64-generic-linux/*/test2json
/V3/usr/lib64/gcc/x86_64-generic-linux/*/vet
/V4/usr/lib64/gcc/x86_64-generic-linux/*/test2json
/V4/usr/lib64/gcc/x86_64-generic-linux/*/vet
/usr/lib64/go/*/x86_64-generic-linux/*.gox
/usr/lib64/go/*/x86_64-generic-linux/*/*.gox
/usr/lib64/go/*/x86_64-generic-linux/*/*/*.gox
/V3/usr/lib64/go/*/x86_64-generic-linux/*.gox
/V3/usr/lib64/go/*/x86_64-generic-linux/*/*.gox
/V3/usr/lib64/go/*/x86_64-generic-linux/*/*/*.gox
/V4/usr/lib64/go/*/x86_64-generic-linux/*.gox
/V4/usr/lib64/go/*/x86_64-generic-linux/*/*.gox
/V4/usr/lib64/go/*/x86_64-generic-linux/*/*/*.gox

/usr/lib64/libgo.a
/usr/lib64/libgo.so
/usr/lib64/libgo.so.*
/usr/lib64/libgobegin.a
/usr/lib64/libgolibbegin.a

#no 32 bit go
%exclude /usr/lib32/go/

#avx2
/V3/usr/lib64/libgo.so.*

#avx512
/V4/usr/lib64/libgo.so.*

%files -n gcc-locale -f gcc.lang

%files libubsan
/usr/lib64/libubsan*so*
/usr/lib64/libasan*so*
/usr/lib64/libtsan*so*
/usr/lib64/liblsan*so*
/usr/lib64/libsanit*
%exclude /V3/usr/lib64/libasan_preinit.o
%exclude /V3/usr/lib64/liblsan_preinit.o
/usr/lib64/libsanitizer.spec
%exclude /V3/usr/lib64/libtsan_preinit.o
%exclude /V4/usr/lib64/libasan_preinit.o
%exclude /V4/usr/lib64/liblsan_preinit.o
/usr/lib64/libsanitizer.spec
%exclude /V4/usr/lib64/libtsan_preinit.o
#avx2
/V3/usr/lib64/libubsan*so*
/V3/usr/lib64/libasan*so*
/V3/usr/lib64/libtsan*so*
/V3/usr/lib64/liblsan*so*

#avx512
/V4/usr/lib64/libubsan*so*
/V4/usr/lib64/libasan*so*
/V4/usr/lib64/libtsan*so*
/V4/usr/lib64/liblsan*so*

/V3/usr/lib64/libhwasan.so.0.0.0
%exclude /V3/usr/lib64/libhwasan_preinit.o
/V4/usr/lib64/libhwasan.so.0.0.0
%exclude /V4/usr/lib64/libhwasan_preinit.o
/usr/lib64/libhwasan.so
/usr/lib64/libhwasan.so.0
/usr/lib64/libhwasan.so.0.0.0


