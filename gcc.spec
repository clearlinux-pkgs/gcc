%define keepstatic 1
%define gcc_target %{_arch}-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.22
%define isl_version 0.14
%define gccver 6.2.0

%define debug_package %{nil}


# Highest optimisation ABI we target
%define mtune haswell

# Lowest compatible ABI (must be lowest of current targets & OBS builders)
# avoton (silvermont target) && ivybridge (OBS builders) = westmere
%define march westmere

Name     : gcc
Version  : 6.2.0
Release  : 19
URL      : http://www.gnu.org/software/gcc/
Source0  : http://ftp.gnu.org/gnu/gcc/gcc-6.2.0/gcc-6.2.0.tar.bz2
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
export LIBRARY_PATH=%{_libdir}

../gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=%{_libdir} \
    --enable-libstdcxx-pch\
    --libexecdir=%{_libdir} \
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
    --exec-prefix=%{_prefix} \
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
export LIBRARY_PATH=%{_libdir}
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

find %{buildroot}%{_prefix}/ -name libiberty.a | xargs rm -f
find %{buildroot}%{_prefix}/ -name libiberty.h | xargs rm -f
chmod 0755 %{buildroot}/usr/lib64/libgcc_s.so.1
chmod 0755 %{buildroot}/usr/lib/libgcc_s.so.1

chmod a+x %{buildroot}/usr/bin
chmod a+x %{buildroot}/usr/lib64
chmod -R a+x %{buildroot}/usr/lib*/gcc/




# This is only for gdb
mkdir -p %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}
mv %{buildroot}/%{_prefix}/lib64/libstdc++.so.%{libstdcxx_full}-gdb.py %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}/.

# clang compat
for i in /usr/lib64/gcc/x86_64-generic-linux/6.2.0/*.o; do ln -s $i %{buildroot}/usr/lib64 ; done
for i in /usr/lib64/gcc/x86_64-generic-linux/6.2.0/*.a; do ln -s $i %{buildroot}/usr/lib64 ; done


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
%{_prefix}/lib64/libatomic*
%{_prefix}/lib64/libitm*
%{_prefix}/lib64/libquadmath*
%{_prefix}/lib64/libcilkrts*
#%{_prefix}/lib64/libvtv*
%{_prefix}/lib64/libcc1*
%{_libdir}/gcc/%{gcc_target}/%{gccver}/include-fixed/
%{_libdir}/gcc/%{gcc_target}/%{gccver}/install-tools/
%{_libdir}/gcc/%{gcc_target}/%{gccver}/libcaf_*
%{_libdir}/gcc/%{gcc_target}/%{gccver}/include/
%{_libdir}/gcc/%{gcc_target}/%{gccver}/lto1
%{_libdir}/gcc/%{gcc_target}/%{gccver}/lto-wrapper
%{_libdir}/gcc/%{gcc_target}/%{gccver}/collect2
%{_libdir}/gcc/%{gcc_target}/%{gccver}/cc1plus
%{_libdir}/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so.0.0.0
%{_libdir}/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so.0
%{_libdir}/gcc/%{gcc_target}/%{gccver}/cc1
%{_libdir}/gcc/%{gcc_target}/%{gccver}/plugin/gtype.state
%{_libdir}/gcc/%{gcc_target}/%{gccver}/plugin/*.so.*
%{_libdir}/gcc/%{gcc_target}/%{gccver}/plugin/include/
%{_datadir}/gcc-%{gccver}
/usr/lib64/*.a
/usr/lib64/*.o


#gfortran
%{_bindir}/%{gcc_target}-gfortran
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/f951
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/finclude
%{_prefix}/lib64/libgfortran*
%{_bindir}/f95
%{_bindir}/gfortran

#g++
%{_bindir}/%{gcc_target}-g++
%{_bindir}/c++
%{_bindir}/g++

# gcc-dev
%{_libdir}/gcc/%{gcc_target}/%{gccver}/liblto_plugin.so
%{_libdir}/gcc/%{gcc_target}/%{gccver}/plugin/*.so

%files -n gcc-dev
# libgcc-s-dev
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/libgcc.a
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtendS.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/libgcc_eh.a
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtprec32.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtend.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtbegin.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtprec80.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtfastmath.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtbeginS.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtprec64.o
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/crtbeginT.o
%{_libdir}/libgcc_s.so
%{_libdir}/gcc/%{_arch}-generic-linux/%{gccver}/libgcov.a
%{_libdir}/gcc/%{gcc_target}/%{gccver}/include/ssp
%{_prefix}/lib64/libssp*.a
/usr/lib64/libmpx.a
/usr/lib64/libgomp.a
/usr/lib64/libmpx.so
/usr/lib64/libmpxwrappers.a
/usr/lib64/libmpxwrappers.so
# gcc-plugin-dev
%{_libdir}/gcc/%{gcc_target}/%{gccver}/plugin/gengtype

# libstdc++
%{_prefix}/lib64/libstdc++.so
%{_prefix}/lib64/libstdc++.a
%{_prefix}/lib64/libsupc++.a
%{_includedir}/c++
%{_datadir}/gdb/auto-load/%{_libdir}/libstdc++.so.*
/usr/lib64/libstdc++fs.a

%files dev32
/usr/lib/libstdc++.a
/usr/lib/libstdc++.so
/usr/lib/libstdc++fs.a
/usr/lib/libsupc++.a
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
/usr/lib/libmpx.a
/usr/lib/libmpx.so
/usr/lib/libasan.a
/usr/lib/libasan.so
/usr/lib/libcilkrts.a
/usr/lib/libcilkrts.so
/usr/lib/libatomic.a
/usr/lib/libatomic.so
/usr/lib/libgfortran.a
/usr/lib/libgfortran.so
/usr/lib/libgomp.a
/usr/lib/libgomp.so
/usr/lib/libitm.a
/usr/lib/libitm.so
/usr/lib/libmpxwrappers.a
/usr/lib/libmpxwrappers.so
/usr/lib/libquadmath.a
/usr/lib/libquadmath.so
/usr/lib/libssp.a
/usr/lib/libssp.so
/usr/lib/libubsan.a
/usr/lib/libubsan.so
#/usr/lib/libvtv.a
#/usr/lib/libvtv.so


%files -n libgcc1
%{_libdir}/libgcc_s.so.1
%{_prefix}/lib64/libssp.so*
%{_prefix}/lib64/libgomp*so*
/usr/lib64/libgomp.spec
/usr/lib64/libmpx.so.2
/usr/lib64/libmpx.so.2.0.0
/usr/lib64/libmpx.spec
/usr/lib64/libmpxwrappers.so.2
/usr/lib64/libmpxwrappers.so.2.0.0

%files libgcc32
/usr/lib/libasan.so.3
/usr/lib/libasan.so.3.0.0
/usr/lib/libasan_preinit.o
/usr/lib/libatomic.so.1
/usr/lib/libatomic.so.1.2.0
/usr/lib/libcilkrts.so.5
/usr/lib/libcilkrts.so.5.0.0
/usr/lib/libcilkrts.spec
/usr/lib/libgcc_s.so
/usr/lib/libgcc_s.so.1
/usr/lib/libgfortran.so.3
/usr/lib/libgfortran.so.3.0.0
/usr/lib/libgfortran.spec
%exclude /usr/lib/libgo.*
%exclude /usr/lib/libgobegin.a
%exclude /usr/lib/libgolibbegin.a
/usr/lib/libgomp.so.1
/usr/lib/libgomp.so.1.0.0
/usr/lib/libgomp.spec
/usr/lib/libitm.so.1
/usr/lib/libitm.so.1.0.0
/usr/lib/libitm.spec
/usr/lib/libmpx.so.2
/usr/lib/libmpx.so.2.0.0
/usr/lib/libmpx.spec
/usr/lib/libmpxwrappers.so.2
/usr/lib/libmpxwrappers.so.2.0.0
%exclude /usr/lib/libnetgo.a
/usr/lib/libquadmath.so.0
/usr/lib/libquadmath.so.0.0.0
/usr/lib/libsanitizer.spec
/usr/lib/libssp.so.0
/usr/lib/libssp.so.0.0.0
/usr/lib/libssp_nonshared.a
/usr/lib/libubsan.so.0
/usr/lib/libubsan.so.0.0.0
#/usr/lib/libvtv.so.0
#/usr/lib/libvtv.so.0.0.0


%files -n libstdc++
%{_prefix}/lib64/libstdc++.so.*

%files libstdc++32
/usr/lib/libstdc++.so.*


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
%exclude /usr/lib/go/

%files go-lib
/usr/lib64/libgo.so.*
/usr/lib64/go/*/%{_arch}-generic-linux/*.gox
/usr/lib64/go/*/%{_arch}-generic-linux/*/*.gox
/usr/lib64/go/*/%{_arch}-generic-linux/*/*/*.gox

%files -n gcc-locale -f gcc.lang

%files libubsan
%{_prefix}/lib64/libubsan*
%{_prefix}/lib64/libasan*
%ifnarch i386
%{_prefix}/lib64/libtsan*
%{_prefix}/lib64/liblsan*
%endif
%{_prefix}/lib64/libsanit*
