Summary:	Muscle PCSC Framework for Linux
Name:		pcsc-lite
Version:	1.1.1
Release:	1
License:	BSD
Group:		System Environment/Daemons
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	rc-scripts
Requires:	pthread-devel

%description
pcscd is the daemon program for PC/SC Lite. It is a resource manager
that coorinates communications with Smart Card readers and Smart Cards
that are connected to the system. The purpose of PCSC Lite is to
provide a Windows(R) SCard interface in a very small form factor for
communicating to smartcards and readers. PCSC Lite uses the same
winscard api as used under Windows(R)

%description -l pl
Pcscd jest demonem dla  PC/SC Lite. Koordynuje on komunikacjê z 
czytnikami Smart Card. Celem pcscd jest udostêpnienie interfejsu
zgodnego z  Windows(R) SCard. Demon ten u¿ywa winscard api, tak
jak Microsoft[TM] Windows(R).

%package devel
Summary:    Development files
Summary(pl):    Pliki dla developerów
Group:      Development/Tools
Requires:   %{name} = %{version}

%description devel
Development files

%description -l pl devel
Pliki dla developerów


%package libs
Summary:    libraries
Summary(pl):    Bibloteki 
Group:      Development/Tools
Requires:   %{name} = %{version}

%description libs
What is a package w/o his libs?

%description -l pl libs
Bo czym¿ jest pakiet bez swoich biblotek ?

%post libs
/sbin/ldconfig

%package static
Summary:    Static libraries
Summary(pl):    Bibloteki statyczne
Group:      Development/Tools
Requires:   %{name} = %{version}

%description static
What is a package w/o -static?

%description -l pl static
Bo czym¿ jest pakiet bez -static ?

%prep
%setup -q

%build

%{configure2_13}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
#install -m 755 etc/pcscd.startup /etc/init.d/pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc0.d/K81pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc1.d/K81pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc2.d/S21pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc3.d/S21pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc4.d/S21pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc5.d/S21pcscd
#ln -sf /etc/init.d/pcscd /etc/rc.d/rc6.d/K81pcscd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/reader.conf
%attr(755,root,root) %{_sbindir}/pcscd
%attr(755,root,root) %{_bindir}/bundleTool
%attr(755,root,root) %{_bindir}/formaticc
%attr(755,root,root) %{_bindir}/installifd

%doc doc/*
%doc AUTHORS DRIVERS NEWS HELP README SECURITY
%{_mandir}/man1/bundleTool.1.gz
%{_mandir}/man8/pcscd.8.gz


%files devel
%{_includedir}/*

%files static
%{_libdir}/*\.a

%files libs
%{_libdir}/*so*
%{_libdir}/libpcsc*\.la

#/etc/init.d/pcscd
#/etc/rc.d/rc0.d/K81pcscd
#/etc/rc.d/rc1.d/K81pcscd
#/etc/rc.d/rc2.d/S21pcscd
#/etc/rc.d/rc3.d/S21pcscd
#/etc/rc.d/rc4.d/S21pcscd
#/etc/rc.d/rc5.d/S21pcscd
#/etc/rc.d/rc6.d/K81pcscd
