Name:           ot-recorder
Version:        0.0.0
Release:        0
Summary:        OwnTracks Recorder
Group:          Applications/Location
License:        MIT
URL:            http://owntracks.org/
Vendor:         OwnTracks team@owntracks.org
Source:         recorder-%{version}.tar.gz
BuildRequires:	lmdb-devel
BuildRequires:	libconfig-devel
BuildRequires:	libsodium-devel
BuildRequires:	libcurl-devel
BuildRequires:  libmosquitto-devel

%if %{defined suse_version}
#Requires:       libopenssl1_0_0
BuildRequires:  libopenssl-devel
%else
#Requires:       openssl
BuildRequires:  openssl-devel
%endif

%description
OwnTracks is a location-based service which runs over MQTT. The
OwnTracks Recorder connects to an MQTT broker and stores location
published from the OwnTracks apps (iOS, Android) into files which
can be viewed through the supporting ocat utility and via a REST
API provided by the Recorder itself.

%prep
%setup -n recorder-%{version}

%build
cp config.mk.in config.mk
make

%install
## make install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
install --strip --mode 0755 ot-recorder %{buildroot}%{_sbindir}
install --strip --mode 0755 ocat %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/doc/owntracks
install --mode 0444 README.md %{buildroot}%{_datadir}/doc/owntracks
mkdir -p %{buildroot}/var/spool/owntracks/recorder/htdocs
cp -R docroot/* %{buildroot}/var/spool/owntracks/recorder/htdocs
mkdir -p %{buildroot}%{_sysconfdir}/default
cp etc/rhel/ot-recorder.defaults %{buildroot}%{_sysconfdir}/default/ot-recorder
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install --mode 0755 etc/rhel/ot-recorder.init %{buildroot}%{_sysconfdir}/init.d/ot-recorder
mkdir -p %{buildroot}/var/spool/owntracks/recorder/store

%clean

%files
%defattr(-,root,owntracks)
%config /etc/default/ot-recorder
%doc    /usr/share/doc/owntracks
/var/spool/owntracks/
%config /var/spool/owntracks/recorder/store
/etc/init.d/ot-recorder
/usr/bin/ocat
/usr/sbin/ot-recorder

%post
getent group owntracks > /dev/null || /usr/sbin/groupadd -r owntracks
mkdir -p /var/spool/owntracks/recorder/store/ghash
chmod 775 /var/spool/owntracks/recorder/store/ghash
chgrp owntracks /var/spool/owntracks/recorder/store
chgrp owntracks /var/spool/owntracks/recorder/store/ghash
chgrp owntracks /usr/bin/ocat /usr/sbin/ot-recorder
chmod 2755 /usr/bin/ocat /usr/sbin/ot-recorder
#chkconfig --add ot-recorder

%changelog
* Wed Aug 19 2020 Danny Sauer <dsauer@suse.com>
- update spec for Open Build Service
- add buildrequires

* Mon Sep 14 2015 Jan-Piet Mens <jpmens@gmail.com>
- munge for OBS (thank you, Roger Light, for your help!)
- relocate spool dir

* Sun Sep 13 2015 Jan-Piet Mens <jpmens@gmail.com>
- remove config.h.example
- use plain config.mk

* Wed Sep 09 2015 Jan-Piet Mens <jpmens@gmail.com>
- Add owntracks group and chmod to SGID for ocat to be able to open LMDB env

* Wed Sep 09 2015 Jan-Piet Mens <jpmens@gmail.com>
- initial spec with tremendous thank yous to https://stereochro.me/ideas/rpm-for-the-unwilling

