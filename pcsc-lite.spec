Summary:	Muscle PCSC Framework for Linux
Summary(pl):	�rodowisko PCSC dla Linuksa
Name:		pcsc-lite
Version:	1.1.1
Release:	1
License:	BSD
Group:		Daemons
Source0:	http://linuxnet.com/middleware/file/%{name}-%{version}.tar.gz
URL:		http://www.linuxnet.com/middle.html
PreReq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R).

%description -l pl
pcscd jest demonem dla PC/SC Lite. Jest to zarz�dca zasob�w,
koordynuj�cy komunikacj� z czytnikami Smart Card pod��czonymi do
systemu. Celem PCSC Lite jest udost�pnienie interfejsu zgodnego z
Windows(R) SCard s�u��cego do komunikacji z czytnikami kart chipowych.
U�ywa tego samego API winscard, kt�re jest u�ywane pod Microsoft[TM]
Windows(R).

%package libs
Summary:	PC/SC Lite libraries
Summary(pl):	Biblioteki PC/SC Lite
Group:		Libraries

%description libs
PC/SC Lite libraries.

%description libs -l pl
Biblioteki PC/SC Lite.

%package devel
Summary:	PC/SC Lite development files
Summary(pl):	Pliki dla programist�w u�ywaj�cych PC/SC Lite
Group:		Development/Tools
Requires:	%{name}-libs = %{version}

%description devel
PC/SC Lite development files.

%description devel -l pl
Pliki dla programist�w u�ywaj�cych PC/SC Lite.

%package static
Summary:	Static PC/SC Lite libraries
Summary(pl):	Biblioteki statyczne PC/SC Lite
Group:		Development/Tools
Requires:	%{name}-devel = %{version}

%description static
Static PC/SC Lite libraries.

%description static -l pl
Statyczne biblioteki PC/SC Lite.

%prep
%setup -q

%build
%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# should have "chkconfig 2345 21 81"
#install -m 755 etc/pcscd.startup /etc/rc.d/init.d/pcscd

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING DRIVERS NEWS HELP README SECURITY doc/{README.DAEMON,*.pdf,pcscd.startup}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/reader.conf
%attr(755,root,root) %{_sbindir}/pcscd
%attr(755,root,root) %{_bindir}/bundleTool
%attr(755,root,root) %{_bindir}/formaticc
%attr(755,root,root) %{_bindir}/installifd
#%attr(754,root,root) /etc/rc.d/init.d/pcscd
%{_mandir}/man1/bundleTool.1*
%{_mandir}/man8/pcscd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/libpcsc*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
