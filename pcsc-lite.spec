Summary:	Muscle PCSC Framework for Linux
Summary(pl):	¦rodowisko PCSC dla Linuksa
Name:		pcsc-lite
Version:	1.1.1
Release:	3
License:	BSD
Group:		Daemons
Source0:	http://linuxnet.com/middleware/file/%{name}-%{version}.tar.gz
# Source0-md5:	3ddbe45100c686230d341bd0e00c472d
Source1:	%{name}-pcscd.init
Source2:	%{name}-pcscd.sysconfig
Patch0:		%{name}-fhs.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-amfix.patch
URL:		http://www.linuxnet.com/middle.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R).

%description -l pl
pcscd jest demonem dla PC/SC Lite. Jest to zarz±dca zasobów,
koordynuj±cy komunikacjê z czytnikami kart procesorowych pod³±czonymi
do systemu. Celem PCSC Lite jest udostêpnienie interfejsu zgodnego z
Windows(R) SCard s³u¿±cego do komunikacji z czytnikami kart chipowych.
U¿ywa tego samego API winscard, które jest u¿ywane pod Microsoft(TM)
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
Summary(pl):	Pliki dla programistów u¿ywaj±cych PC/SC Lite
Group:		Development/Tools
Requires:	%{name}-libs = %{version}

%description devel
PC/SC Lite development files.

%description devel -l pl
Pliki dla programistów u¿ywaj±cych PC/SC Lite.

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/pcsc/{drivers,services} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# useful for drivers development
install src/ifdhandler.h $RPM_BUILD_ROOT%{_includedir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcscd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcscd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pcscd
if [ -f /var/lock/subsys/pcscd ]; then
	/etc/rc.d/init.d/pcscd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pcscd start\" to start pcscd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pcscd ]; then
		/etc/rc.d/init.d/pcscd stop >&2
	fi
	/sbin/chkconfig --del pcscd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING DRIVERS NEWS HELP README SECURITY doc/{README.DAEMON,*.pdf,pcscd.startup}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/reader.conf
%attr(754,root,root) /etc/rc.d/init.d/pcscd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pcscd
%attr(755,root,root) %{_sbindir}/pcscd
%attr(755,root,root) %{_bindir}/bundleTool
%attr(755,root,root) %{_bindir}/formaticc
%attr(755,root,root) %{_bindir}/installifd
%{_libdir}/pcsc
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
