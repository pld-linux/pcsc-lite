# TODO
# - follow upstream with using /run instead of /var/run
# - pcscd & pcscd-lite-libs need to be exactly same version installed otherwise
#   client will flood daemon so much that daemon is not usable (max 200
#   connections reached, etc)
#
# Conditional build:
%bcond_without	polkit	# polkit support
%bcond_without	systemd	# libsystemd support
%bcond_without	udev	# udev support (plain libusb if disabled)

Summary:	PCSC Framework for Linux
Summary(pl.UTF-8):	Środowisko PCSC dla Linuksa
Name:		pcsc-lite
Version:	2.0.0
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://pcsclite.apdu.fr/files/%{name}-%{version}.tar.bz2
# Source0-md5:	45bf7ef136537f68a26976d89f631cbf
Source1:	%{name}-pcscd.init
Source2:	%{name}-pcscd.sysconfig
Source4:	%{name}.tmpfiles
Patch1:		%{name}-any.patch
Patch2:		debuglog-pid.patch
URL:		https://pcsclite.apdu.fr/
BuildRequires:	autoconf >= 2.69
BuildRequires:	autoconf-archive
BuildRequires:	automake >= 1:1.8
BuildRequires:	flex
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	libtool >= 2:2.0
%{!?with_udev:BuildRequires:	libusb-devel >= 1.0}
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_polkit:BuildRequires:	polkit-devel >= 0.111}
BuildRequires:	rpmbuild(macros) >= 1.647
%{?with_systemd:BuildRequires:	systemd-devel}
%{?with_udev:BuildRequires:	udev-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(pretrans):	fileutils
%{?with_polkit:Requires:	polkit >= 0.111}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		usbdropdir	/usr/%{_lib}/pcsc/drivers

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R).

%description -l pl.UTF-8
pcscd jest demonem dla PC/SC Lite. Jest to zarządca zasobów,
koordynujący komunikację z czytnikami kart procesorowych podłączonymi
do systemu. Celem PCSC Lite jest udostępnienie interfejsu zgodnego z
Windows(R) SCard służącego do komunikacji z czytnikami kart chipowych.
Używa tego samego API winscard, które jest używane pod Microsoft(TM)
Windows(R).

%package libs
Summary:	PC/SC Lite libraries
Summary(pl.UTF-8):	Biblioteki PC/SC Lite
Group:		Libraries

%description libs
PC/SC Lite libraries.

%description libs -l pl.UTF-8
Biblioteki PC/SC Lite.

%package devel
Summary:	PC/SC Lite development files
Summary(pl.UTF-8):	Pliki dla programistów używających PC/SC Lite
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
PC/SC Lite development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających PC/SC Lite.

%package static
Summary:	Static PC/SC Lite libraries
Summary(pl.UTF-8):	Biblioteki statyczne PC/SC Lite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PC/SC Lite libraries.

%description static -l pl.UTF-8
Statyczne biblioteki PC/SC Lite.

%package apidocs
Summary:	PC/SC Lite API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PC/SC Lite
Group:		Documentation

%description apidocs
API and internal documentation for PC/SC Lite library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PC/SC Lite.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%{__sed} -i -e '1s, /usr/bin/python$,%{__python3},' src/spy/pcsc-spy

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# auto power down unreliable yet
CPPFLAGS="%{rpmcppflags} -DDISABLE_ON_DEMAND_POWER_ON"
%configure \
	%{!?with_systemd:--disable-libsystemd} \
	%{!?with_udev:--disable-libudev} \
	--disable-silent-rules \
	--enable-ipcdir=/var/run/pcscd \
	%{?with_polkit:--enable-polkit} \
	--enable-static \
	--enable-usbdropdir=%{usbdropdir}

%{__make}

%if %{with apidocs}
doxygen doc/doxygen.conf
rm -f doc/api/*.{map,md5}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{usbdropdir} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d \
	$RPM_BUILD_ROOT/var/run/pcscd \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcscd
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcscd
install %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

cp -p doc/example/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# upgrade from pcsc-lite < 1.2.9-0.beta7
if [ -f /etc/reader.conf -a ! -f %{_sysconfdir}/reader.conf.d/reader.conf ]; then
	install -d -m755 %{_sysconfdir}/reader.conf.d
	cp -af /etc/reader.conf %{_sysconfdir}/reader.conf.d/reader.conf
fi

%post
/sbin/chkconfig --add pcscd
%service pcscd restart "PC/SC smart card daemon"
%systemd_post pcscd.service pcscd.socket

%preun
if [ "$1" = "0" ]; then
	%service pcscd stop
	/sbin/chkconfig --del pcscd
fi
%systemd_preun pcscd.service pcscd.socket

%postun
%systemd_reload

%triggerpostun -- pcsc-lite < 1.8.3-1
%systemd_trigger pcscd.service pcscd.socket

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog HELP README SECURITY TODO doc/README.polkit
%attr(755,root,root) %{_bindir}/pcsc-spy
%attr(755,root,root) %{_sbindir}/pcscd
%dir %{_libdir}/pcsc
%dir %{_libdir}/pcsc/drivers
%dir %{_sysconfdir}/reader.conf.d
%attr(754,root,root) /etc/rc.d/init.d/pcscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pcscd
%{_mandir}/man1/pcsc-spy.1*
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*
%dir /var/run/pcscd
%{systemdunitdir}/pcscd.service
%{systemdunitdir}/pcscd.socket
/usr/lib/tmpfiles.d/%{name}.conf
%if %{with polkit}
%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcsclite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcsclite.so.1
%attr(755,root,root) %{_libdir}/libpcscspy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcscspy.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcsclite.so
%attr(755,root,root) %{_libdir}/libpcscspy.so
%{_libdir}/libpcsclite.la
%{_libdir}/libpcscspy.la
%{_includedir}/PCSC
%{_pkgconfigdir}/libpcsclite.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcsclite.a
%{_libdir}/libpcscspy.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/api/*
%endif
