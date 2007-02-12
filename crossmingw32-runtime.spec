Summary:	Mingw32 Binary Utility Development Utilities - runtime libraries
Summary(pl.UTF-8):	Zestaw narzędzi mingw32 - biblioteki uruchomieniowe
Name:		crossmingw32-runtime
Version:	3.10
%define runver	%{version}
%define	runsrc	mingw-runtime-%{runver}
Release:	1
Epoch:		1
License:	Free
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/mingw/%{runsrc}-src.tar.gz
# Source0-md5:	9225684e663eafa900b4075731c25f4c
Patch0:		%{name}-stdinc.patch
Patch1:		%{name}-configure.patch
URL:		http://www.mingw.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-binutils
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	dos2unix
Requires:	crossmingw32-binutils >= 2.15.91.0.2-2
Requires:	crossmingw32-w32api >= 3.1
Obsoletes:	crossmingw32-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32
%define		_prefix			/usr/%{target}
%define		_libdir			%{_prefix}/lib

# strip fails on static COFF files
%define		no_install_post_strip 1

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains MinGW32 runtime includes and libraries.

%description -l pl.UTF-8
crossmingw32 jest kompletnym systemem do kompilacji skrośnej,
pozwalającym budować aplikacje MS Windows pod Linuksem używając
bibliotek mingw32. System składa się z binutils, gcc z g++ i objc,
libstdc++ - wszystkie generujące kod dla platformy i386-mingw32, oraz
z bibliotek w formacie COFF.

Ten pakiet zawiera pliki nagłówkowe i biblioteki uruchomieniowe
MinGW32.

%prep
%setup -q -n %{runsrc}
dos2unix Makefile.in configure.in mkinstalldirs */Makefile.in */configure.in
%patch0 -p1 
%patch1 -p1

%build
cp /usr/share/automake/config.sub .
%{__autoconf}
cd mingwex
cp /usr/share/automake/config.sub .
%{__autoconf}
cd ../profile
cp /usr/share/automake/config.sub .
%{__autoconf}
cd ..
./configure \
	--prefix=%{_prefix} \
	--host=%{target} \
	--build=%{_target_platform}
%{__make} -C mingwex
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

%if %{!?debug:1}0
%{target}-strip $RPM_BUILD_ROOT%{_bindir}/*.dll
%{target}-strip -g $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog DISCLAIMER README TODO readme.txt
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*
