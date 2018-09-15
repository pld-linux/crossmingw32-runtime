Summary:	MinGW32 Binary Utility Development Utilities - runtime libraries
Summary(pl.UTF-8):	Zestaw narzędzi MinGW32 - biblioteki uruchomieniowe
Name:		crossmingw32-runtime
Version:	5.0.2
Release:	1
Epoch:		1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/mingw/mingwrt-%{version}-mingw32-src.tar.xz
# Source0-md5:	9865c83624b0e80178fdc709ebbc5e15
Patch0:		%{name}-gawk.patch
Patch1:		%{name}-stdinc.patch
# http://sourceforge.net/p/mingw/bugs/2122/, adapted for 5.0.x, change errno_t header to <sys/types.h>
Patch2:		rand_s-mingw.patch
URL:		http://www.mingw.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	crossmingw32-binutils
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api >= 1:%{version}
BuildRequires:	dos2unix
Requires:	crossmingw32-binutils >= 2.15.91.0.2-2
Requires:	crossmingw32-w32api >= 1:%{version}
Obsoletes:	crossmingw32-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32
%define		_prefix			/usr/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system

# strip fails on static COFF files
%define		no_install_post_strip 1

# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]* -gdwarf-3

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the MinGW32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains MinGW32 runtime includes and libraries.

%description -l pl.UTF-8
crossmingw32 jest kompletnym systemem do kompilacji skrośnej,
pozwalającym budować aplikacje MS Windows pod Linuksem używając
bibliotek MinGW32. System składa się z binutils, gcc z g++ i objc,
libstdc++ - wszystkie generujące kod dla platformy i386-mingw32, oraz
z bibliotek w formacie COFF.

Ten pakiet zawiera pliki nagłówkowe i biblioteki uruchomieniowe
MinGW32.

%package dll
Summary:	MinGW32 runtime DLL library for Windows
Summary(pl.UTF-8):	Biblioteka uruchomieniowa MingW32 DLL dla Windows
Group:		Applications/Emulators

%description dll
MinGW32 runtime DLL library for Windows.

%description dll -l pl.UTF-8
Biblioteka uruchomieniowa MingW32 DLL dla Windows.

%prep
%setup -q -n mingwrt-%{version}
dos2unix Makefile.in configure.ac */Makefile.in
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
cp %{_includedir}/w32api.h w32api.h.in
cp /usr/share/automake/config.sub .
%{__autoconf}
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--host=%{target} \
	--build=%{_target_platform}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
# makefile expects dir before creating it
#install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if %{!?debug:1}0
%{target}-strip $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog DISCLAIMER README TODO readme.txt
%{_includedir}/_mingw.h
%{_includedir}/assert.h
%{_includedir}/complex.h
%{_includedir}/conio.h
%{_includedir}/ctype.h
%{_includedir}/dir.h
%{_includedir}/direct.h
%{_includedir}/dirent.h
%{_includedir}/dlfcn.h
%{_includedir}/dos.h
%{_includedir}/errno.h
%{_includedir}/excpt.h
%{_includedir}/fcntl.h
%{_includedir}/fenv.h
%{_includedir}/float.h
%{_includedir}/getopt.h
%{_includedir}/glob.h
%{_includedir}/gmon.h
%{_includedir}/inttypes.h
%{_includedir}/io.h
%{_includedir}/libgen.h
%{_includedir}/limits.h
%{_includedir}/locale.h
%{_includedir}/malloc.h
%{_includedir}/math.h
%{_includedir}/mbctype.h
%{_includedir}/mbstring.h
%{_includedir}/mem.h
%{_includedir}/memory.h
%{_includedir}/msvcrtver.h
%{_includedir}/process.h
%{_includedir}/profil.h
%{_includedir}/profile.h
%{_includedir}/search.h
%{_includedir}/setjmp.h
%{_includedir}/share.h
%{_includedir}/signal.h
%{_includedir}/stdint.h
%{_includedir}/stdio.h
%{_includedir}/stdlib.h
%{_includedir}/string.h
%{_includedir}/strings.h
%{_includedir}/tchar.h
%{_includedir}/time.h
%{_includedir}/unistd.h
%{_includedir}/utime.h
%{_includedir}/values.h
%{_includedir}/wchar.h
%{_includedir}/wctype.h
%{_includedir}/sys
%{_libdir}/CRT_*.o
%{_libdir}/binmode.o
%{_libdir}/crt*.o
%{_libdir}/dllcrt*.o
%{_libdir}/gcrt*.o
%{_libdir}/txtmode.o
%{_libdir}/libcoldname.a
%{_libdir}/libcrtdll.a
%{_libdir}/libgmon.a
%{_libdir}/libm.a
%{_libdir}/libmingw*.a
%{_libdir}/libmoldname*.a
%{_libdir}/libmsvcr*.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/mingwm10.dll
