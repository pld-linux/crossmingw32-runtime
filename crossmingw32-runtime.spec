Summary:	Mingw32 Binary Utility Development Utilities - runtime libraries
Summary(pl):	Zestaw narzêdzi mingw32 - biblioteki uruchomieniowe
Name:		crossmingw32-runtime
Version:	3.0
#%%define	run_date	20010604
#%%define	runsrc		mingw-runtime-%{version}-%{run_date}
%define runver	%{version}
%define	runsrc	mingw-runtime-%{runver}
Release:	1
Epoch:		1
License:	Free
Group:		Development/Libraries
# requires cross-gcc installed... loop. Use binaries (doesn't change much, I think).
#Source0:	http://dl.sourceforge.net/mingw/%{runsrc}-src.tar.gz
Source0:	http://dl.sourceforge.net/mingw/%{runsrc}.tar.gz
URL:		http://www.mingw.org/
ExclusiveArch:	%{ix86}
Obsoletes:	crossmingw32-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		i386-mingw32
%define		target_platform i386-pc-mingw32
%define		arch		%{_prefix}/%{target}

# strip fails on static COFF files
%define		no_install_post_strip 1

%description
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains MinGW32 runtime includes and libraries.

%description -l pl
crossmingw32 jest kompletnym systemem do kroskompilacji, pozwalaj±cym
budowaæ aplikacje MS Windows pod Linuksem u¿ywaj±c bibliotek mingw32.
System sk³ada siê z binutils, gcc z g++ i objc, libstdc++ - wszystkie
generuj±ce kod dla platformy i386-mingw32, oraz z bibliotek w formacie
COFF.

Ten pakiet zawiera pliki nag³ówkowe i biblioteki uruchomieniowe
MinGW32.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{bin,include,lib}

cp -fa include/* $RPM_BUILD_ROOT%{arch}/include
cp -fa lib/* bin/*.dll $RPM_BUILD_ROOT%{arch}/lib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}
