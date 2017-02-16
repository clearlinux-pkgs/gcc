%define keepstatic 1
%define gcc_target %{_arch}-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.22
%define isl_version 0.14
%define gccver 6.3.0

%define debug_package %{nil}


# Highest optimisation ABI we target
%define mtune haswell

# Lowest compatible ABI (must be lowest of current targets & OBS builders)
# avoton (silvermont target) && ivybridge (OBS builders) = westmere
%define march westmere

Name     : gcc
Version  : 6.3.0
Release  : 27
URL      : http://www.gnu.org/software/gcc/
Source0  : http://ftp.gnu.org/gnu/gcc/gcc-6.3.0/gcc-6.3.0.tar.bz2
Source1  : ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Summary  : GNU cc and gcc C compilers
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT
Patch0   : 0001-Fix-stack-protection-issues.patch
Patch2   : openmp-vectorize.patch
Patch3   : fortran-vector.patch
Patch5   : optimize.patch
Patch6   : ipa-cp.patch
Patch7   : max-is-safe-on-x86.patch
Patch8	 : optimize-at-least-some.patch
Patch9   : gcc6-SOURCE_DATE_EPOCH.patch
Patch10  : randomseed.patch

BuildRequires : bison
BuildRequires : flex
BuildRequires : gmp-dev
BuildRequires : libstdc++
BuildRequires : libunwind-dev
BuildRequires : mpc-dev
BuildRequires : mpfr-dev
BuildRequires : pkgconfig(zlib)
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

Requires: gcc-libubsan
Requires: gcc-doc

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

%description
GNU cc and gcc C compilers.

%package -n gcc-dev
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libgcov-dev
Provides:       libssp-dev
Provides:       libssp-staticdev
Provides:       libgomp-dev
Provides:       libgomp-staticdev
Provides:       libgcc-s-dev
Provides:       gcc-plugin-dev

Provides:       libstdc++-dev

%description -n gcc-dev
GNU cc and gcc C compilers dev files



%package dev32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

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

%package -n gcc-locale
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description -n gcc-locale
GNU cc and gcc C compilers.


%prep
%setup -q -n gcc-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p0
%patch10 -p1



%build

# Live in the gcc source tree
tar xf %{SOURCE1} && ln -sf isl-%{isl_version} isl

rm -rf ../gcc-build
mkdir ../gcc-build
pushd ../gcc-build
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=westmere -g1 -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000"
export CXXFLAGS="-march=westmere -g1 -O3  -Wl,-z,max-page-size=0x1000"
export CFLAGS_FOR_TARGET="$CFLAGS"

export CPATH=%{_includedir}
export LIBRARY_PATH=/usr/lib64

../gcc-%{version}/configure \
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
    --enable-lto\
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-languages="c,c++,fortran,go" \
    --enable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --includedir=%{_includedir} \
    --with-gxx-include-dir=%{_includedir}/c++/ \
    --exec-prefix=/usr \
    --with-glibc-version=2.19 \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=westmere \
    --enable-libmpx

make %{?_smp_mflags} profiledbootstrap

popd

%check
pushd ../gcc-build
export CHECK_TEST_FRAMEWORK=1
make -k  %{?_smp_mflags} check  || :
popd


%install
export CPATH=%{_includedir}
export LIBRARY_PATH=/usr/lib64
pushd ../gcc-build
%make_install
cd -

cd %{buildroot}%{_bindir}
if [ -e %{gcc_target}-g77 ]; then
    ln -sf %{gcc_target}-g77 g77 || true
    ln -sf g77 f77 || true
fi
if [ -e %{_arch}-generic-linux-gfortran ]; then
    ln -sf %{gcc_target}-gfortran gfortran || true
    ln -sf gfortran f95 || true
fi
ln -sf %{gcc_target}-g++ g++
ln -sf %{gcc_target}-gcc gcc
#ln -sf %{gcc_target}-cpp cpp
install -d %{buildroot}/lib
ln -sf /usr/bin/cpp %{buildroot}/lib/cpp
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
chmod 0755 %{buildroot}/usr/lib64/libgcc_s.so.1
chmod 0755 %{buildroot}/usr/lib32/libgcc_s.so.1

chmod a+x %{buildroot}/usr/bin
chmod a+x %{buildroot}/usr/lib64
chmod -R a+x %{buildroot}/usr/lib*/gcc/




# This is only for gdb
mkdir -p %{buildroot}/%{_datadir}/gdb/auto-load//usr/lib64
mkdir -p %{buildroot}/%{_datadir}/gdb/auto-load//usr/lib32
mv %{buildroot}//usr/lib64/libstdc++.so.%{libstdcxx_full}-gdb.py %{buildroot}/%{_datadir}/gdb/auto-load//usr/lib64/.
mv %{buildroot}//usr/lib32/libstdc++.so.%{libstdcxx_full}-gdb.py %{buildroot}/%{_datadir}/gdb/auto-load//usr/lib32/.

# clang compat
for i in /usr/lib64/gcc/x86_64-generic-linux/6.3.0/*.o; do ln -s $i %{buildroot}/usr/lib64 ; done
for i in /usr/lib64/gcc/x86_64-generic-linux/6.3.0/*.a; do ln -s $i %{buildroot}/usr/lib64 ; done


%find_lang cpplib cpp.lang
%find_lang gcc tmp.lang
%find_lang libstdc++ cxx.lang
cat *.lang > gcc.lang

%files
%{_bindir}/%{gcc_target}-gcc-ar
%{_bindir}/%{gcc_target}-gcc-ranlib
%{_bindir}/%{gcc_target}-gcc-nm
%{_bindir}/%{gcc_target}-gcc
%{_bindir}/%{gcc_target}-c++
%{_bindir}/%{gcc_target}-gcc-%{gccver}
%{_bindir}/gcc
%{_bindir}/cc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_bindir}/gcov-tool
/lib/cpp
%{_bindir}/cpp
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
/usr/lib64/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so.0.0.0
/usr/lib64/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so.0
/usr/lib64/gcc/%{gcc_target}/%{gccver}/cc1
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gtype.state
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so.*
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/include/
%{_datadir}/gcc-%{gccver}
/usr/lib64/*.a
/usr/lib64/*.o


#gfortran
%{_bindir}/%{gcc_target}-gfortran
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/f951
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/finclude
/usr/lib64/libgfortran*
%{_bindir}/f95
%{_bindir}/gfortran

#g++
%{_bindir}/%{gcc_target}-g++
%{_bindir}/c++
%{_bindir}/g++

# gcc-dev
/usr/lib64/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/*.so

%files -n gcc-dev
# libgcc-s-dev
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/libgcc.a
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtendS.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/libgcc_eh.a
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtprec32.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtend.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtbegin.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtprec80.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtfastmath.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtbeginS.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtprec64.o
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/crtbeginT.o
/usr/lib64/libgcc_s.so
/usr/lib64/gcc/%{_arch}-generic-linux/%{gccver}/libgcov.a
/usr/lib64/gcc/%{gcc_target}/%{gccver}/include/ssp
/usr/lib64/libssp*.a
/usr/lib64/libmpx.a
/usr/lib64/libgomp.a
/usr/lib64/libmpx.so
/usr/lib64/libmpxwrappers.a
/usr/lib64/libmpxwrappers.so
# gcc-plugin-dev
/usr/lib64/gcc/%{gcc_target}/%{gccver}/plugin/gengtype
/usr/lib64/libcilkrts*.so.*

# libstdc++
/usr/lib64/libstdc++.so
/usr/lib64/libstdc++.a
/usr/lib64/libsupc++.a
%{_includedir}/c++
%{_datadir}/gdb/auto-load//usr/lib64/libstdc++.so.*
/usr/lib64/libstdc++fs.a

%files dev32
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
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_arithmetic.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_exceptions.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/finclude/ieee_features.mod
/usr/lib64/gcc/x86_64-generic-linux/*/32/libcaf_single.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcc.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcc_eh.a
/usr/lib64/gcc/x86_64-generic-linux/*/32/libgcov.a
/usr/lib32/libmpx.a
/usr/lib32/libmpx.so
/usr/lib32/libasan.a
/usr/lib32/libasan.so
/usr/lib32/libcilkrts.a
/usr/lib32/libcilkrts.so
/usr/lib32/libatomic.a
/usr/lib32/libatomic.so
/usr/lib32/libgfortran.a
/usr/lib32/libgfortran.so
/usr/lib32/libgomp.a
/usr/lib32/libgomp.so
/usr/lib32/libitm.a
/usr/lib32/libitm.so
/usr/lib32/libmpxwrappers.a
/usr/lib32/libmpxwrappers.so
/usr/lib32/libquadmath.a
/usr/lib32/libquadmath.so
/usr/lib32/libssp.a
/usr/lib32/libssp.so
/usr/lib32/libubsan.a
/usr/lib32/libubsan.so
/usr/lib64/libatomic.so
/usr/lib64/libcilkrts.so
/usr/lib64/libcilkrts.spec
/usr/lib64/libitm.so
/usr/lib64/libitm.spec
/usr/lib64/libquadmath.so

#/usr/lib/libvtv.a
#/usr/lib/libvtv.so
%{_datadir}/gdb/auto-load//usr/lib32/libstdc++.so.*


%files -n libgcc1
/usr/lib64/libgcc_s.so.1
/usr/lib64/libssp.so*
/usr/lib64/libgomp*so*
/usr/lib64/libgomp.spec
/usr/lib64/libmpx.so.2
/usr/lib64/libmpx.so.2.0.0
/usr/lib64/libmpx.spec
/usr/lib64/libmpxwrappers.so.2
/usr/lib64/libmpxwrappers.so.2.0.0
/usr/lib64/libatomic*.so.*
/usr/lib64/libitm*.so.*
/usr/lib64/libquadmath*.so.*

%files libgcc32
/usr/lib32/libasan.so.3
/usr/lib32/libasan.so.3.0.0
/usr/lib32/libasan_preinit.o
/usr/lib32/libatomic.so.1
/usr/lib32/libatomic.so.1.2.0
/usr/lib32/libcilkrts.so.5
/usr/lib32/libcilkrts.so.5.0.0
/usr/lib32/libcilkrts.spec
/usr/lib32/libgcc_s.so
/usr/lib32/libgcc_s.so.1
/usr/lib32/libgfortran.so.3
/usr/lib32/libgfortran.so.3.0.0
/usr/lib32/libgfortran.spec
%exclude /usr/lib32/libgo.*
%exclude /usr/lib32/libgobegin.a
%exclude /usr/lib32/libgolibbegin.a
/usr/lib32/libgomp.so.1
/usr/lib32/libgomp.so.1.0.0
/usr/lib32/libgomp.spec
/usr/lib32/libitm.so.1
/usr/lib32/libitm.so.1.0.0
/usr/lib32/libitm.spec
/usr/lib32/libmpx.so.2
/usr/lib32/libmpx.so.2.0.0
/usr/lib32/libmpx.spec
/usr/lib32/libmpxwrappers.so.2
/usr/lib32/libmpxwrappers.so.2.0.0
%exclude /usr/lib32/libnetgo.a
/usr/lib32/libquadmath.so.0
/usr/lib32/libquadmath.so.0.0.0
/usr/lib32/libsanitizer.spec
/usr/lib32/libssp.so.0
/usr/lib32/libssp.so.0.0.0
/usr/lib32/libssp_nonshared.a
/usr/lib32/libubsan.so.0
/usr/lib32/libubsan.so.0.0.0
#/usr/lib/libvtv.so.0
#/usr/lib/libvtv.so.0.0.0


%files -n libstdc++
/usr/lib64/libstdc++.so.*

%files libstdc++32
/usr/lib32/libstdc++.so.*


%files -n gcc-doc
%{_mandir}/man1
%{_mandir}/man7
%{_infodir}

%files go
/usr/libexec/gccgo/bin/*
/usr/bin/gccgo
/usr/bin/%{_arch}-generic-linux-gccgo
/usr/lib64/gcc/%{_arch}-generic-linux/*/cgo
/usr/lib64/gcc/%{_arch}-generic-linux/*/go1
/usr/lib64/libgo.a
/usr/lib64/libgo.so
/usr/lib64/libgobegin.a
/usr/lib64/libgolibbegin.a
/usr/lib64/libnetgo.a
#no 32 bit go
%exclude /usr/lib32/go/

%files go-lib
/usr/lib64/libgo.so.*
/usr/lib64/go/*/%{_arch}-generic-linux/*.gox
/usr/lib64/go/*/%{_arch}-generic-linux/*/*.gox
/usr/lib64/go/*/%{_arch}-generic-linux/*/*/*.gox

%files -n gcc-locale -f gcc.lang

%files libubsan
/usr/lib64/libubsan*
/usr/lib64/libasan*
%ifnarch i386
/usr/lib64/libtsan*
/usr/lib64/liblsan*
%endif
/usr/lib64/libsanit*
