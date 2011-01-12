#
# Conditional build:
%bcond_without	hal	# use libusb instead of HAL

Summary:	PCSC Framework for Linux
Summary(pl.UTF-8):	Środowisko PCSC dla Linuksa
Name:		pcsc-lite
Version:	1.6.6
Release:	0.2
License:	BSD
Group:		Daemons
# Source0Download: http://alioth.debian.org/project/showfiles.php?group_id=30105
Source0:	http://alioth.debian.org/download.php/3479/%{name}-%{version}.tar.bz2
# Source0-md5:	f80d3ecd9569b71d557f283f16295c74
Source1:	%{name}-pcscd.init
Source2:	%{name}-pcscd.sysconfig
Patch0:		%{name}-fhs.patch
Patch1:		%{name}-any.patch
Patch2:		noautostart.patch
URL:		http://www.linuxnet.com/middle.html
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1:1.8
BuildRequires:	flex
%{?with_apidocs:BuildRequires:	graphviz}
%{?with_hal:BuildRequires:	hal-devel}
BuildRequires:	libtool >= 1.4.2-9
%{!?with_hal:BuildRequires:	libusb-devel >= 1.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(pretrans):	fileutils
Requires:	rc-scripts
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_hal:--disable-libhal} \
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
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcscd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcscd

cp -a doc/example/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# upgrade from pcsc-lite < 1.2.9-0.beta7
if [ -f /etc/reader.conf -a ! -f /etc/reader.conf.d/reader.conf ]; then
	install -d -m755 /etc/reader.conf.d
	cp -af /etc/reader.conf /etc/reader.conf.d/reader.conf
fi

%post
/sbin/chkconfig --add pcscd
%service pcscd restart "PC/SC smart card daemon"

%preun
if [ "$1" = "0" ]; then
	%service pcscd stop
	/sbin/chkconfig --del pcscd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog* DRIVERS HELP NEWS README SECURITY TODO doc/README.DAEMON
%attr(755,root,root) %{_sbindir}/pcscd
%dir %{_libdir}/pcsc
%dir %{_libdir}/pcsc/drivers
%dir %{_sysconfdir}/reader.conf.d
%attr(754,root,root) /etc/rc.d/init.d/pcscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pcscd
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcsclite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcsclite.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/example/pcsc_demo.c
%attr(755,root,root) %{_libdir}/libpcsclite.so
%{_libdir}/libpcsclite.la
%{_includedir}/PCSC
%{_pkgconfigdir}/libpcsclite.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcsclite.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/api/*
%endif
