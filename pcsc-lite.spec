Summary:	Muscle PCSC Framework for Linux
Summary(pl):	�rodowisko PCSC dla Linuksa
Name:		pcsc-lite
Version:	1.2.9
%define	bver	beta6
Release:	0.%{bver}.1
License:	BSD
Group:		Daemons
#Source0Download: http://alioth.debian.org/project/showfiles.php?group_id=1225
Source0:	http://alioth.debian.org/download.php/753/%{name}-%{version}-%{bver}.tar.gz
# Source0-md5:	ba8896b9382bc5d6e6d1159013e23e10
Source1:	%{name}-pcscd.init
Source2:	%{name}-pcscd.sysconfig
Patch0:		%{name}-fhs.patch
URL:		http://www.linuxnet.com/middle.html
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool >= 1.4.2-9
BuildRequires:	libusb-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		muscledropdir	/usr/%{_lib}/pcsc/services
%define		usbdropdir	/usr/%{_lib}/pcsc/drivers

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R).

%description -l pl
pcscd jest demonem dla PC/SC Lite. Jest to zarz�dca zasob�w,
koordynuj�cy komunikacj� z czytnikami kart procesorowych pod��czonymi
do systemu. Celem PCSC Lite jest udost�pnienie interfejsu zgodnego z
Windows(R) SCard s�u��cego do komunikacji z czytnikami kart chipowych.
U�ywa tego samego API winscard, kt�re jest u�ywane pod Microsoft(TM)
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
Requires:	%{name}-libs = %{version}-%{release}

%description devel
PC/SC Lite development files.

%description devel -l pl
Pliki dla programist�w u�ywaj�cych PC/SC Lite.

%package static
Summary:	Static PC/SC Lite libraries
Summary(pl):	Biblioteki statyczne PC/SC Lite
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PC/SC Lite libraries.

%description static -l pl
Statyczne biblioteki PC/SC Lite.

%prep
%setup -q -n %{name}-%{version}-%{bver}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-muscledropdir=%{muscledropdir} \
	--enable-runpid=/var/run/pcscd.pid \
	--enable-usbdropdir=%{usbdropdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{muscledropdir},%{usbdropdir}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcscd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcscd

install doc/example/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
%doc AUTHORS COPYING ChangeLog* DRIVERS HELP NEWS README SECURITY doc/README.DAEMON
%attr(755,root,root) %{_bindir}/formaticc
%attr(755,root,root) %{_sbindir}/bundleTool
%attr(755,root,root) %{_sbindir}/installifd
%attr(755,root,root) %{_sbindir}/pcscd
%{_libdir}/pcsc
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/reader.conf
%attr(754,root,root) /etc/rc.d/init.d/pcscd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pcscd
%{_mandir}/man1/formaticc.1*
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/bundleTool.8*
%{_mandir}/man8/pcscd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/*.pdf
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/PCSC
%{_pkgconfigdir}/*.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
