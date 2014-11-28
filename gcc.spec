%define keepstatic 1
%define gcc_target x86_64-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.21
%define isl_version 0.14

%define debug_package %{nil}


# Highest optimisation ABI we target
%define mtune haswell

# Lowest compatible ABI (must be lowest of current targets & OBS builders)
# avoton (silvermont target) && ivybridge (OBS builders) = westmere
%define march westmere

Name     : gcc
Version  : 5.2.0
Release  : 51
URL      : http://www.gnu.org/software/gcc/
Source0  : http://ftp.gnu.org/gnu/gcc/gcc-5.2.0/gcc-5.2.0.tar.bz2
Source1  : ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Summary  : GNU cc and gcc C compilers
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT
Patch0   : 0001-Fix-stack-protection-issues.patch
Patch1   : multiver_gcc5.patch

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


%package -n libgcc1
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Requires:       filesystem
Provides:       libssp0
Provides:       libgomp1

%description -n libgcc1
GNU cc and gcc C compilers.


%package -n libstdc++
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libstdc++-extra

%description -n libstdc++
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
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build

# Live in the gcc source tree
tar xf %{SOURCE1} && ln -sf isl-%{isl_version} isl

mkdir ../gcc-build
pushd ../gcc-build
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=ivybridge -g -O2 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000"
export CXXFLAGS="-march=ivybridge -g -O2  -Wl,-z,max-page-size=0x1000"

export CPATH=%{_includedir}
export LIBRARY_PATH=%{_libdir}

../%{name}-%{version}/configure \
    --prefix=%{_prefix} \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=%{_libdir} \
    --enable-libstdcxx-pch\
    --libexecdir=%{_libdir} \
    --with-system-zlib\
    --enable-shared\
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --disable-multilib\
    --enable-lto\
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-languages="c,c++,fortran,go" \
    --enable-bootstrap \
    --with-ppl=no \
    --includedir=%{_includedir} \
    --with-gxx-include-dir=%{_includedir}/c++/ \
    --exec-prefix=%{_prefix} \
    --with-glibc-version=2.19 \
    --with-system-libunwind \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=ivybridge \
    --enable-libmpx

make %{?_smp_mflags}

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
if [ -e x86_64-generic-linux-gfortran ]; then
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
chmod 0755 %{buildroot}/%{_libdir}/libgcc_s.so.1

chmod a+x %{buildroot}/usr/bin
chmod a+x %{buildroot}/usr/lib64
chmod -R a+x %{buildroot}/usr/lib64/gcc/




# This is only for gdb
mkdir -p %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}
mv %{buildroot}/%{_prefix}/lib64/libstdc++.so.%{libstdcxx_full}-gdb.py %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}/.

%find_lang cpplib cpp.lang
%find_lang gcc tmp.lang
%find_lang libstdc++ cxx.lang
cat *.lang > %{name}.lang

%files
%{_bindir}/%{gcc_target}-gcc-ar
%{_bindir}/%{gcc_target}-gcc-ranlib
%{_bindir}/%{gcc_target}-gcc-nm
%{_bindir}/%{gcc_target}-gcc
%{_bindir}/%{gcc_target}-c++
%{_bindir}/%{gcc_target}-gcc-%{version}
%{_bindir}/gcc
%{_bindir}/cc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_bindir}/gcov-tool
/lib/cpp
%{_bindir}/cpp
%{_prefix}/lib64/libasan*
%{_prefix}/lib64/libtsan*
%{_prefix}/lib64/libatomic*
%{_prefix}/lib64/libitm*
%{_prefix}/lib64/libquadmath*
%{_prefix}/lib64/libcilkrts*
%{_prefix}/lib64/liblsan*
%{_prefix}/lib64/libsanit*
%{_prefix}/lib64/libubsan*
%{_prefix}/lib64/libvtv*
%{_prefix}/lib64/libcc1*
%{_libdir}/gcc/%{gcc_target}/%{version}/include-fixed/
%{_libdir}/gcc/%{gcc_target}/%{version}/install-tools/
%{_libdir}/gcc/%{gcc_target}/%{version}/libcaf_*
%{_libdir}/gcc/%{gcc_target}/%{version}/include/
%{_libdir}/gcc/%{gcc_target}/%{version}/lto1
%{_libdir}/gcc/%{gcc_target}/%{version}/lto-wrapper
%{_libdir}/gcc/%{gcc_target}/%{version}/collect2
%{_libdir}/gcc/%{gcc_target}/%{version}/cc1plus
%{_libdir}/gcc/%{gcc_target}/%{version}/liblto_plugin.so.0.0.0
%{_libdir}/gcc/%{gcc_target}/%{version}/liblto_plugin.so.0
%{_libdir}/gcc/%{gcc_target}/%{version}/cc1
%{_libdir}/gcc/%{gcc_target}/%{version}/plugin/gtype.state
%{_libdir}/gcc/%{gcc_target}/%{version}/plugin/*.so.*
%{_libdir}/gcc/%{gcc_target}/%{version}/plugin/include/
%{_datadir}/%{name}-%{version}

#gfortran
%{_bindir}/%{gcc_target}-gfortran
%{_libdir}/gcc/x86_64-generic-linux/%{version}/f951
%{_libdir}/gcc/x86_64-generic-linux/%{version}/finclude
%{_prefix}/lib64/libgfortran*
%{_libdir}/gcc/%{gcc_target}/%{version}/libgfortran*
%{_bindir}/f95
%{_bindir}/gfortran

#g++
%{_bindir}/%{gcc_target}-g++
%{_bindir}/c++
%{_bindir}/g++

# gcc-dev
%{_libdir}/gcc/%{gcc_target}/%{version}/liblto_plugin.so
%{_libdir}/gcc/%{gcc_target}/%{version}/plugin/*.so

%files -n gcc-dev
# libgcc-s-dev
%{_libdir}/gcc/x86_64-generic-linux/%{version}/libgcc.a
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtendS.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/libgcc_eh.a
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtprec32.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtend.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtbegin.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtprec80.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtfastmath.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtbeginS.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtprec64.o
%{_libdir}/gcc/x86_64-generic-linux/%{version}/crtbeginT.o
%{_libdir}/libgcc_s.so
%{_libdir}/gcc/x86_64-generic-linux/%{version}/libgcov.a
%{_libdir}/gcc/%{gcc_target}/%{version}/include/ssp
%{_prefix}/lib64/libssp*.a
/usr/lib64/libmpx.a
/usr/lib64/libmpx.so
/usr/lib64/libmpxwrappers.a
/usr/lib64/libmpxwrappers.so
# gcc-plugin-dev
%{_libdir}/gcc/%{gcc_target}/%{version}/plugin/gengtype

# libstdc++
%{_prefix}/lib64/libstdc++.so
%{_prefix}/lib64/libstdc++.a
%{_prefix}/lib64/libsupc++.a
%{_includedir}/c++
%{_datadir}/gdb/auto-load/%{_libdir}/libstdc++.so.*

%files -n libgcc1
%{_libdir}/libgcc_s.so.1
%{_prefix}/lib64/libssp.so*
%{_prefix}/lib64/libgomp*
/usr/lib64/libmpx.so.0
/usr/lib64/libmpx.so.0.0.0
/usr/lib64/libmpx.spec
/usr/lib64/libmpxwrappers.so.0
/usr/lib64/libmpxwrappers.so.0.0.0

%files -n libstdc++
%{_prefix}/lib64/libstdc++.so.*

%files -n gcc-doc
%{_mandir}/man1
%{_mandir}/man7
%{_infodir}

%files go
/usr/libexec/gccgo/bin/*
/usr/bin/gccgo
/usr/bin/x86_64-generic-linux-gccgo
/usr/lib64/gcc/x86_64-generic-linux/5.2.0/cgo
/usr/lib64/gcc/x86_64-generic-linux/5.2.0/go1
/usr/lib64/libgo.a
/usr/lib64/libgo.so
/usr/lib64/libgobegin.a
/usr/lib64/libgolibbegin.a
/usr/lib64/libnetgo.a

%files go-lib
/usr/lib64/libgo.so.*
/usr/lib64/go/*/x86_64-generic-linux/*.gox
/usr/lib64/go/*/x86_64-generic-linux/*/*.gox
/usr/lib64/go/*/x86_64-generic-linux/*/*/*.gox

%files -n gcc-locale -f %{name}.lang
