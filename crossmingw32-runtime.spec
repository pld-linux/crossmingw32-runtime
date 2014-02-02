Summary:	MinGW32 Binary Utility Development Utilities - runtime libraries
Summary(pl.UTF-8):	Zestaw narzędzi MinGW32 - biblioteki uruchomieniowe
Name:		crossmingw32-runtime
Version:	4.0.3
Release:	1
Epoch:		1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/mingw/mingwrt-%{version}-1-mingw32-src.tar.lzma
# Source0-md5:	118e3ef1f632b08fe3cd53560eb54c40
Source1:	http://www.opengl.org/registry/api/GL/glext.h
Source2:	http://www.opengl.org/registry/api/GL/wglext.h
Patch0:		%{name}-format.patch
Patch1:		crossmingw32-w32api-mmsystem.patch
URL:		http://www.mingw.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	crossmingw32-binutils
BuildRequires:	crossmingw32-gcc
BuildRequires:	dos2unix
Requires:	crossmingw32-binutils >= 2.15.91.0.2-2
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

%package -n crossmingw32-w32api
Summary:	MinGW32 Binary Utility Development Utilities - Win32 API libraries
Summary(pl.UTF-8):	Zestaw narzędzi MinGW32 - biblioteki API Win32
Group:		Development/Libraries
Requires:	crossmingw32-runtime = %{epoch}:%{version}-%{release}
Obsoletes:	crossmingw32-platform

%description -n crossmingw32-w32api
crossmingw32 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the MinGW32 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to i386-mingw32, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains Win32 API includes and libraries.

%description -n crossmingw32-w32api -l pl.UTF-8
crossmingw32 jest kompletnym systemem do kompilacji skrośnej,
pozwalającym budować aplikacje MS Windows pod Linuksem używając
bibliotek MinGW32. System składa się z binutils, gcc z g++ i objc,
libstdc++ - wszystkie generujące kod dla platformy i386-mingw32, oraz
z bibliotek w formacie COFF.

Ten pakiet zawiera pliki nagłówkowe i biblioteki Win32 API.

%package -n crossmingw32-w32api-dx
Summary:	DirectX from MinGW Win32 API
Summary(pl.UTF-8):	DirectX z API Win32 dla MinGW
Group:		Development/Libraries
Requires:	crossmingw32-w32api = %{epoch}:%{version}-%{release}
Provides:	crossmingw32-dx
Obsoletes:	crossmingw32-dx

%description -n crossmingw32-w32api-dx
DirectX from MinGW Win32 API.

%description -n crossmingw32-w32api-dx -l pl.UTF-8
DirectX z API Win32 dla MinGW.

%prep
%setup -q -n mingwrt-%{version}-1-mingw32-src
dos2unix Makefile.in configure.ac */Makefile.in
%patch0 -p1
%patch1 -p1

%build
cp /usr/share/automake/config.sub .
%{__autoconf}
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--host=%{target} \
	--build=%{_target_platform}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# makefile expects dir before creating it
install -d $RPM_BUILD_ROOT%{_includedir}/GL

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if %{!?debug:1}0
%{target}-strip $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/GL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE NEWS NOTES README TODO
%{_includedir}/_mingw.h
%{_includedir}/assert.h
%{_includedir}/complex.h
%{_includedir}/conio.h
%{_includedir}/ctype.h
%{_includedir}/dir.h
%{_includedir}/direct.h
%{_includedir}/dirent.h
%{_includedir}/dos.h
%{_includedir}/errno.h
%{_includedir}/fcntl.h
%{_includedir}/fenv.h
%{_includedir}/float.h
%{_includedir}/getopt.h
%{_includedir}/glob.h
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
%{_includedir}/process.h
%{_includedir}/profil.h
%{_includedir}/profile.h
%{_includedir}/sdkddkver.h
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
%{_includedir}/varargs.h
%{_includedir}/wchar.h
%{_includedir}/wctype.h
%{_includedir}/sys
%{_libdir}/CRT_*.o
%{_libdir}/binmode.o
%{_libdir}/crt*.o
%{_libdir}/dllcrt*.o
%{_libdir}/gcrt*.o
%{_libdir}/ofmt_stub.o
%{_libdir}/txtmode.o
%{_libdir}/libgmon.a
%{_libdir}/libm.a
%{_libdir}/libmingw*.a
%{_libdir}/libmoldname*.a
%{_libdir}/libmsvcr*.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/mingwm10.dll

%files -n crossmingw32-w32api
%defattr(644,root,root,755)
%{_libdir}/libaclui.a
%{_libdir}/libadvapi32.a
%{_libdir}/libapcups.a
%{_libdir}/libavicap32.a
%{_libdir}/libavifil32.a
%{_libdir}/libbthprops.a
%{_libdir}/libcap.a
%{_libdir}/libcfgmgr32.a
%{_libdir}/libcomctl32.a
%{_libdir}/libcomdlg32.a
%{_libdir}/libcrypt32.a
%{_libdir}/libctl3d32.a
%{_libdir}/libdhcpcsvc.a
%{_libdir}/libdlcapi.a
%{_libdir}/libdnsapi.a
%{_libdir}/libdxapi.a
%{_libdir}/libfaultrep.a
%{_libdir}/libgdi32.a
%{_libdir}/libgdiplus.a
%{_libdir}/libglaux.a
%{_libdir}/libglu32.a
%{_libdir}/libhal.a
%{_libdir}/libhid.a
%{_libdir}/libhidparse.a
%{_libdir}/libicmui.a
%{_libdir}/libigmpagnt.a
%{_libdir}/libimagehlp.a
%{_libdir}/libimm32.a
%{_libdir}/libiphlpapi.a
%{_libdir}/libkernel32.a
%{_libdir}/libksproxy.a
%{_libdir}/libksuser.a
%{_libdir}/liblargeint.a
%{_libdir}/liblz32.a
%{_libdir}/libmapi32.a
%{_libdir}/libmcd.a
%{_libdir}/libmfcuia32.a
%{_libdir}/libmgmtapi.a
%{_libdir}/libmpr.a
%{_libdir}/libmprapi.a
%{_libdir}/libmqrt.a
%{_libdir}/libmsacm32.a
%{_libdir}/libmscms.a
%{_libdir}/libmsdmo.a
%{_libdir}/libmsimg32.a
%{_libdir}/libmsvcp60.a
%{_libdir}/libmsvfw32.a
%{_libdir}/libmswsock.a
%{_libdir}/libnddeapi.a
%{_libdir}/libndis.a
%{_libdir}/libnetapi32.a
%{_libdir}/libnewdev.a
%{_libdir}/libntdll.a
%{_libdir}/libntoskrnl.a
%{_libdir}/libodbc32.a
%{_libdir}/libodbccp32.a
%{_libdir}/libole32.a
%{_libdir}/liboleacc.a
%{_libdir}/liboleaut32.a
%{_libdir}/libolecli32.a
%{_libdir}/liboledlg.a
%{_libdir}/libolepro32.a
%{_libdir}/libolesvr32.a
%{_libdir}/libopengl32.a
%{_libdir}/libpenwin32.a
%{_libdir}/libpkpd32.a
%{_libdir}/libpowrprof.a
%{_libdir}/libpsapi.a
%{_libdir}/libquartz.a
%{_libdir}/librapi.a
%{_libdir}/librasapi32.a
%{_libdir}/librasdlg.a
%{_libdir}/librpcdce4.a
%{_libdir}/librpcns4.a
%{_libdir}/librpcrt4.a
%{_libdir}/librtm.a
%{_libdir}/librtutils.a
%{_libdir}/libscrnsave.a
%{_libdir}/libscrnsavw.a
%{_libdir}/libscsiport.a
%{_libdir}/libsecur32.a
%{_libdir}/libsetupapi.a
%{_libdir}/libshell32.a
%{_libdir}/libshfolder.a
%{_libdir}/libshlwapi.a
%{_libdir}/libsnmpapi.a
%{_libdir}/libstrmiids.a
%{_libdir}/libsvrapi.a
%{_libdir}/libtapi32.a
%{_libdir}/libtdi.a
%{_libdir}/libthunk32.a
%{_libdir}/liburl.a
%{_libdir}/libusbcamd.a
%{_libdir}/libusbcamd2.a
%{_libdir}/libuser32.a
%{_libdir}/libuserenv.a
%{_libdir}/libusp10.a
%{_libdir}/libuuid.a
%{_libdir}/libuxtheme.a
%{_libdir}/libvdmdbg.a
%{_libdir}/libversion.a
%{_libdir}/libvfw32.a
%{_libdir}/libvideoprt.a
%{_libdir}/libwin32k.a
%{_libdir}/libwin32spl.a
%{_libdir}/libwininet.a
%{_libdir}/libwinmm.a
%{_libdir}/libwinspool.a
%{_libdir}/libwinstrm.a
%{_libdir}/libwldap32.a
%{_libdir}/libwow32.a
%{_libdir}/libws2_32.a
%{_libdir}/libwsnmp32.a
%{_libdir}/libwsock32.a
%{_libdir}/libwst.a
%{_libdir}/libwtsapi32.a
%dir %{_includedir}
%{_includedir}/accctrl.h
%{_includedir}/aclapi.h
%{_includedir}/aclui.h
%{_includedir}/adsprop.h
%{_includedir}/afxres.h
%{_includedir}/amaudio.h
%{_includedir}/amvideo.h
%{_includedir}/audevcod.h
%{_includedir}/aviriff.h
%{_includedir}/aygshell.h
%{_includedir}/basetsd.h
%{_includedir}/basetyps.h
%{_includedir}/bdatypes.h
%{_includedir}/cderr.h
%{_includedir}/cguid.h
%{_includedir}/cmnquery.h
%{_includedir}/comcat.h
%{_includedir}/commctrl.h
%{_includedir}/commdlg.h
%{_includedir}/control.h
%{_includedir}/cpl.h
%{_includedir}/cplext.h
%{_includedir}/custcntl.h
%{_includedir}/dbt.h
%{_includedir}/dde.h
%{_includedir}/ddeml.h
%{_includedir}/devguid.h
%{_includedir}/dhcpcsdk.h
%{_includedir}/dlgs.h
%{_includedir}/docobj.h
%{_includedir}/dsadmin.h
%{_includedir}/dsclient.h
%{_includedir}/dsgetdc.h
%{_includedir}/dsquery.h
%{_includedir}/dsrole.h
%{_includedir}/dvdevcod.h
%{_includedir}/dvdmedia.h
%{_includedir}/edevdefs.h
%{_includedir}/errorrep.h
%{_includedir}/errors.h
%{_includedir}/evcode.h
%{_includedir}/excpt.h
%{_includedir}/exdisp.h
%{_includedir}/exdispid.h
%{_includedir}/fltdefs.h
%{_includedir}/gdiplus.h
%{_includedir}/httpext.h
%{_includedir}/icm.h
%{_includedir}/idispids.h
%{_includedir}/il21dec.h
%{_includedir}/imagehlp.h
%{_includedir}/imm.h
%{_includedir}/initguid.h
%{_includedir}/intshcut.h
%{_includedir}/ipexport.h
%{_includedir}/iphlpapi.h
%{_includedir}/ipifcons.h
%{_includedir}/ipinfoid.h
%{_includedir}/iprtrmib.h
%{_includedir}/iptypes.h
%{_includedir}/ipxconst.h
%{_includedir}/ipxrtdef.h
%{_includedir}/ipxtfflt.h
%{_includedir}/isguids.h
%{_includedir}/ks.h
%{_includedir}/ksmedia.h
%{_includedir}/largeint.h
%{_includedir}/lm.h
%{_includedir}/lmaccess.h
%{_includedir}/lmalert.h
%{_includedir}/lmapibuf.h
%{_includedir}/lmat.h
%{_includedir}/lmaudit.h
%{_includedir}/lmbrowsr.h
%{_includedir}/lmchdev.h
%{_includedir}/lmconfig.h
%{_includedir}/lmcons.h
%{_includedir}/lmerr.h
%{_includedir}/lmerrlog.h
%{_includedir}/lmmsg.h
%{_includedir}/lmremutl.h
%{_includedir}/lmrepl.h
%{_includedir}/lmserver.h
%{_includedir}/lmshare.h
%{_includedir}/lmsname.h
%{_includedir}/lmstats.h
%{_includedir}/lmsvc.h
%{_includedir}/lmuse.h
%{_includedir}/lmuseflg.h
%{_includedir}/lmwksta.h
%{_includedir}/lzexpand.h
%{_includedir}/mapi.h
%{_includedir}/mciavi.h
%{_includedir}/mcx.h
%{_includedir}/mgm.h
%{_includedir}/mgmtapi.h
%{_includedir}/mlang.h
%{_includedir}/mmreg.h
%{_includedir}/mmsystem.h
%{_includedir}/mpegtype.h
%{_includedir}/mprapi.h
%{_includedir}/mq.h
%{_includedir}/msacm.h
%{_includedir}/mshtml.h
%{_includedir}/mswsock.h
%{_includedir}/nb30.h
%{_includedir}/nddeapi.h
%{_includedir}/nspapi.h
%{_includedir}/ntdef.h
%{_includedir}/ntdll.h
%{_includedir}/ntdsapi.h
%{_includedir}/ntdsbcli.h
%{_includedir}/ntldap.h
%{_includedir}/ntsecapi.h
%{_includedir}/ntsecpkg.h
%{_includedir}/oaidl.h
%{_includedir}/objbase.h
%{_includedir}/objfwd.h
%{_includedir}/objidl.h
%{_includedir}/objsafe.h
%{_includedir}/objsel.h
%{_includedir}/ocidl.h
%{_includedir}/odbcinst.h
%{_includedir}/ole.h
%{_includedir}/ole2.h
%{_includedir}/ole2ver.h
%{_includedir}/oleacc.h
%{_includedir}/oleauto.h
%{_includedir}/olectl.h
%{_includedir}/olectlid.h
%{_includedir}/oledlg.h
%{_includedir}/oleidl.h
%{_includedir}/pbt.h
%{_includedir}/poppack.h
%{_includedir}/powrprof.h
%{_includedir}/prsht.h
%{_includedir}/psapi.h
%{_includedir}/pshpack1.h
%{_includedir}/pshpack2.h
%{_includedir}/pshpack4.h
%{_includedir}/pshpack8.h
%{_includedir}/qedit.h
%{_includedir}/rapi.h
%{_includedir}/ras.h
%{_includedir}/rasdlg.h
%{_includedir}/raserror.h
%{_includedir}/rassapi.h
%{_includedir}/reason.h
%{_includedir}/regstr.h
%{_includedir}/richedit.h
%{_includedir}/richole.h
%{_includedir}/routprot.h
%{_includedir}/rpc.h
%{_includedir}/rpcdce.h
%{_includedir}/rpcdce2.h
%{_includedir}/rpcdcep.h
%{_includedir}/rpcndr.h
%{_includedir}/rpcnsi.h
%{_includedir}/rpcnsip.h
%{_includedir}/rpcnterr.h
%{_includedir}/rpcproxy.h
%{_includedir}/rtutils.h
%{_includedir}/schannel.h
%{_includedir}/schnlsp.h
%{_includedir}/scrnsave.h
%{_includedir}/sddl.h
%{_includedir}/secext.h
%{_includedir}/security.h
%{_includedir}/servprov.h
%{_includedir}/setupapi.h
%{_includedir}/shellapi.h
%{_includedir}/shldisp.h
%{_includedir}/shlguid.h
%{_includedir}/shlobj.h
%{_includedir}/shlwapi.h
%{_includedir}/shobjidl.h
%{_includedir}/snmp.h
%{_includedir}/specstrings.h
%{_includedir}/sql.h
%{_includedir}/sqlext.h
%{_includedir}/sqltypes.h
%{_includedir}/sqlucode.h
%{_includedir}/sspi.h
%{_includedir}/stm.h
%{_includedir}/strmif.h
%{_includedir}/subauth.h
%{_includedir}/svcguid.h
%{_includedir}/tlhelp32.h
%{_includedir}/tmschema.h
%{_includedir}/unknwn.h
%{_includedir}/userenv.h
%{_includedir}/usp10.h
%{_includedir}/uxtheme.h
%{_includedir}/vfw.h
%{_includedir}/vidcap.h
%{_includedir}/vmr9.h
%{_includedir}/vptype.h
%{_includedir}/w32api.h
%{_includedir}/winable.h
%{_includedir}/winbase.h
%{_includedir}/winber.h
%{_includedir}/wincon.h
%{_includedir}/wincrypt.h
%{_includedir}/windef.h
%{_includedir}/windns.h
%{_includedir}/windows.h
%{_includedir}/windowsx.h
%{_includedir}/winerror.h
%{_includedir}/wingdi.h
%{_includedir}/wininet.h
%{_includedir}/winioctl.h
%{_includedir}/winldap.h
%{_includedir}/winnetwk.h
%{_includedir}/winnls.h
%{_includedir}/winnt.h
%{_includedir}/winperf.h
%{_includedir}/winreg.h
%{_includedir}/winresrc.h
%{_includedir}/winsnmp.h
%{_includedir}/winsock.h
%{_includedir}/winsock2.h
%{_includedir}/winspool.h
%{_includedir}/winsvc.h
%{_includedir}/winuser.h
%{_includedir}/winver.h
%{_includedir}/ws2spi.h
%{_includedir}/ws2tcpip.h
%{_includedir}/wsahelp.h
%{_includedir}/wsipx.h
%{_includedir}/wsnetbs.h
%{_includedir}/wtsapi32.h
%{_includedir}/wtypes.h
%{_includedir}/xprtdefs.h
%{_includedir}/zmouse.h
%{_includedir}/GL
%{_includedir}/ddk
%{_includedir}/gdiplus
%files -n crossmingw32-w32api-dx
%defattr(644,root,root,755)
%{_libdir}/libd3d8.a
%{_libdir}/libd3d9.a
%{_libdir}/libd3dim.a
%{_libdir}/libd3drm.a
%{_libdir}/libd3dx8d.a
%{_libdir}/libd3dx9d.a
%{_libdir}/libd3dxof.a
%{_libdir}/libddraw.a
%{_libdir}/libdinput.a
%{_libdir}/libdinput8.a
%{_libdir}/libdmoguids.a
%{_libdir}/libdplayx.a
%{_libdir}/libdpnaddr.a
%{_libdir}/libdpnet.a
%{_libdir}/libdpnlobby.a
%{_libdir}/libdpvoice.a
%{_libdir}/libdsetup.a
%{_libdir}/libdsound.a
%{_libdir}/libdxerr8.a
%{_libdir}/libdxerr9.a
%{_libdir}/libdxguid.a
%{_includedir}/dshow.h
%{_includedir}/directx
