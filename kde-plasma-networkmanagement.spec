Name:           kde-plasma-networkmanagement
Epoch:          1
Version:        0.9.0.9
Release:        7%{?dist}
Summary:        NetworkManager KDE 4 integration

License:        (GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and LGPLv2
URL:            https://projects.kde.org/projects/extragear/base/networkmanagement 

# yes, 0.9.0 is still under "unstable"
Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/networkmanagement-%{version}.tar.bz2

# Add plasma-nm to default systray if needed, for upgraders...
Source10: 00-fedora-networkmanagement.js

## upstream patches
# Display IPv6 information in details
Patch1: kde-plasma-networkmanagement-0.9.0.9-ipv6-details.patch
#Fix crash when creating WPA2 Enterprise connections
Patch2: kde-plasma-networkmanagement-0.9.0.0-bz#916275.patch
#Add Libreswan VPN support
Patch3: kde-plasma-networkmanagement-0.9.0.9-libreswan.patch

BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  kde-workspace-devel
# use pkgconfig() to avoid need for tracking nm epoch
BuildRequires:  pkgconfig(NetworkManager) >= 0.9.0
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util) 
%if 0%{?fedora} || 0%{?epel}
BuildRequires:  pkgconfig(openconnect) >= 3.99
%endif

# multilib upgrades
Obsoletes: kde-plasma-networkmanagement < 0.1-0.21
Obsoletes: kde-plasma-networkmanagement-devel < 0.1-0.21

Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}

Obsoletes: knetworkmanager < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  knetworkmanager = %{?epoch:%{epoch}:}%{version}-%{release}

%description
A Plasma applet to control your wired and wireless network(s) in KDE 4 using
the default NetworkManager service.

%package libs
Summary: Runtime libraries for %{name}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
Obsoletes: knetworkmanager-libs < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  knetworkmanager-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: NetworkManager
%description libs
%{summary}.

# Required for properly working GMS/CDMA connections
%package mobile
Summary: Mobile support for %{name}
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: ModemManager
Requires: mobile-broadband-provider-info
%description mobile
%{summary}.

%if 0%{?fedora} || 0%{?epel}
%package openvpn
Summary:        OpenVPN support for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:       NetworkManager-openvpn
Obsoletes:      knetworkmanager-openvpn < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       knetworkmanager-openvpn = %{?epoch:%{epoch}:}%{version}-%{release}
%description openvpn
%{summary}.

%package pptp
Summary:        PPTP support for %{name} 
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       NetworkManager-pptp
Obsoletes:      knetworkmanager-pptp < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       knetworkmanager-pptp = %{?epoch:%{epoch}:}%{version}-%{release}
%description pptp
%{summary}.

%package vpnc
Summary:        Vpnc support for %{name} 
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:       NetworkManager-vpnc
Obsoletes:      knetworkmanager-vpnc < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       knetworkmanager-vpnc = %{?epoch:%{epoch}:}%{version}-%{release}
%description vpnc
%{summary}.

%package openconnect
Summary:        OpenConnect support for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:       NetworkManager-openconnect
%description openconnect
%{summary}.
%endif

%package libreswan
Summary:        Libreswan support for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:       NetworkManager-libreswan
%description libreswan
%{summary}.

%prep
%setup -q -n networkmanagement-%{version}

%patch1 -p1 -b .ipv6-details
%patch2 -p1 -b .bz#916275
%patch3 -p1 -b .libreswan

%build
if [ -x %{_bindir}/plasma-dataengine-depextractor ] ; then
  plasma-dataengine-depextractor qml/package 
fi

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} .. 
popd


make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

# migrate to nm plasmoid
install -m644 -p -D %{SOURCE10} %{buildroot}%{_kde4_appsdir}/plasma-desktop/updates/00-fedora-networkmanagement.js

%find_lang libknetworkmanager
%find_lang plasma_applet_networkmanagement
%find_lang solidcontrolnm09

cat libknetworkmanager.lang solidcontrolnm09.lang > libs.lang

## unpackaged files
# knetworkmanager locales
rm -fv %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/knetworkmanager.*
# nuke -devel type stuff for which there isn't a public API
rm -rfv %{buildroot}%{_kde4_includedir}/solid/controlnm09
rm -fv %{buildroot}%{_kde4_libdir}/libknm{client,internals,service,ui}.so
# novellvpn bits (TODO: what is it?)
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_novellvpnui.so
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_novellvpnui.desktop
# strongswan bits
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_strongswanui.so
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_strongswanui.desktop

# clean unpackaged VPN related files in RHEL
%if 0%{?rhel}
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_openvpn*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_openconnect*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_pptp*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_vpnc*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_openvpn*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_openconnect*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_pptp*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_vpnc*
%endif


%post
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :

%files -f plasma_applet_networkmanagement.lang
%doc TODO DESIGN COPYING COPYING.LIB
%{_kde4_datadir}/kde4/services/plasma-applet-networkmanagement.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-networkmanagement.desktop
%{_kde4_datadir}/kde4/services/kded/networkmanagement.desktop
%{_kde4_libdir}/kde4/plasma_applet_networkmanagement.so
%{_kde4_libdir}/kde4/plasma_engine_networkmanagement.so
%{_kde4_libdir}/kde4/kded_networkmanagement.so
%{_kde4_appsdir}/plasma-desktop/updates/*.js
%{_kde4_appsdir}/desktoptheme/default/icons/network2.svgz
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_libexecdir}/networkmanagement_configshell
%{_kde4_appsdir}/networkmanagement/
%{_kde4_datadir}/kde4/services/kcm_networkmanagement.desktop
%{_kde4_datadir}/kde4/services/kcm_networkmanagement_tray.desktop
%{_kde4_datadir}/kde4/servicetypes/networkmanagement_vpnuiplugin.desktop
%{_kde4_libdir}/kde4/kcm_networkmanagement.so
%{_kde4_libdir}/kde4/kcm_networkmanagement_tray.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f libs.lang
%{_kde4_libdir}/libknmclient.so.4*
%{_kde4_libdir}/libknminternals.so.4*
%{_kde4_libdir}/libknmservice.so.4*
%{_kde4_libdir}/libknmui.so.4*
%{_kde4_libdir}/libsolidcontrolnm09*
# Unversioned libraries
%{_kde4_libdir}/libknm_nm.so
%{_kde4_libdir}/libsolidcontrolfuture.so
%{_kde4_libdir}/kde4/solid_networkmanager09.so
# desktop files
%{_kde4_datadir}/kde4/services/solidbackends/solid_networkmanager09.desktop
%{_kde4_datadir}/kde4/servicetypes/solidnetworkmanagernm09.desktop

%files mobile
%{_kde4_libdir}/kde4/solid_modemmanager05.so
%{_kde4_datadir}/kde4/services/solidbackends/solid_modemmanager05.desktop
%{_kde4_datadir}/kde4/servicetypes/solidmodemmanagernm09.desktop

%if 0%{?fedora} || 0%{?epel}
%files openvpn
%{_kde4_libdir}/kde4/networkmanagement_openvpnui.so
%{_kde4_datadir}/kde4/services/networkmanagement_openvpnui.desktop

%files vpnc
%{_kde4_libdir}/kde4/networkmanagement_vpncui.so
%{_kde4_datadir}/kde4/services/networkmanagement_vpncui.desktop

%files openconnect
%{_kde4_libdir}/kde4/networkmanagement_openconnectui.so
%{_kde4_datadir}/kde4/services/networkmanagement_openconnectui.desktop

%files pptp
%{_kde4_libdir}/kde4/networkmanagement_pptpui.so
%{_kde4_datadir}/kde4/services/networkmanagement_pptpui.desktop
%endif

%files libreswan
%{_kde4_libdir}/kde4/networkmanagement_libreswanui.so
%{_kde4_datadir}/kde4/services/networkmanagement_libreswanui.desktop

%changelog
* Wed Mar 12 2014 Jan Grulich <jgrulich@redhat.com> 0.9.0.0-7
- Rename openswan to libreswan

* Mon Feb 10 2014 Jan Grulich <jgrulich@redhat.com> 0.9.0.0-6
- Add OpenSwan VPN support
- Resolves #1061697

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:0.9.0.9-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.9.0.9-4
- Mass rebuild 2013-12-27

* Thu Nov 28 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.0-3
- Fix crash when creating WPA2 Enterprise connections
- Resolves #916275

* Fri Sep 27 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.9-2
- Display IPv6 information in connection details
- Resolves #916245

* Sun Jun 16 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.9-1
- 0.9.0.9

* Mon May 13 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.8-3
- add mobile subpkg to have ModemManager dependencies optional

* Sun May 12 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.8-2
- remove mobile-broadband-mobile-provider-devel as BR
- add ModemManager as runtime dependency
- add mobile-broadband-mobile-provider as runtime dependency

* Sat Mar 16 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.8-1
- 0.9.0.8

* Mon Feb 25 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.7-3
- really fix #bz832893

* Tue Feb 19 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.7-2
- fix the wpa2 bug with missing password field #bz832893
- fix the bug with lock indicator #bz912603

* Sun Jan 27 2013 Jan Grulich <jgrulich@redhat.com> 0.9.0.7-1
- 0.9.0.7

* Sat Jan 05 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.6-1
- 0.9.0.6

* Thu Dec 06 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.5-3
- backport upstream vpn-related fixes (#882308)

* Fri Nov 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.5-2
- +plasma-dataengine-depextractor support

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.5-1
- 0.9.0.5

* Mon Jul 30 2012 Lukas Tinkl <ltinkl@redhat.com> 0.9.0.4-1
- upstream version 0.9.0.4 (see
  http://lamarque-lvs.blogspot.cz/2012/07/plasma-nm-0904.html for details)

* Tue Jul 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.3-4
- rebuild

* Mon Jul 02 2012 David Woodhouse <dwmw2@infradead.org> 0.9.0.3-3
- Bump to build against new openconnect on F16/F17

* Mon Jun 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.3-2
- upstream patch to fix build for older openconnect

* Mon Jun 18 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.9.0.3-1
- update to 0.9.0.3
- Password dialog is missing password field (#832893, kde#299868)

* Thu Jun 14 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.0.2-3
- Merge OpenConnect fixes to build with new libopenconnect

* Tue May 22 2012 Lukas Tinkl <ltinkl@redhat.com> 0.9.0.2-2
- add RHEL/Fedora condition

* Mon May 07 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0.2-1
- 0.9.0.2

* Mon Apr 23 2012 Than Ngo <than@redhat.com> - 0.9.0.1-2
- add rhel/fedora condition

* Tue Apr 10 2012 Rex Dieter <rdieter@fedoraproject.org> 1:0.9.0.1-1
- 0.9.0.1
- simplify/pkgconfig'ize deps a bit

* Mon Feb 27 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9.0-1
- update to 0.9.0

* Sun Jan 22 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.70.rc4
- update to 0.9.0_rc4 (0.8.99)
- drop the nm09 tag, all our builds are NM 0.9 builds now
- drop the nuking of monolithic stuff, already disabled upstream for a while

* Sun Jan 08 2012 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.69.20120108git.nm09
- 20120108 snapshot

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.68.20111227git.nm09
- 20111227 snapshot

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.67.20111203git.nm09
- 20111203 snapshot

* Sun Nov 27 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.66.rc3.nm09
- Update to 0.9 rc3 (0.8.98) for NM 0.9

* Fri Nov 04 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.65.rc2.nm09
- update to 0.9 rc 2 (0.8.95) for NM 0.9

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-0.64.beta2.nm09
- Rebuilt for glibc bug#747377

* Sat Oct 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.63.beta2.nm09
- update to 0.9 beta 2 / rc 1 (0.8.90) for NM 0.9

* Sat Oct 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.62.beta1.nm09
- fix plasma-desktop crash after installing updates with apper (kde#284743)

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.61.beta1.nm09
- fill in full URL for Source0

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.60.beta1.nm09
- update to 0.9 beta 1 (0.8.80) for NM 0.9

* Mon Sep 19 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.59.20110919git.nm09
- update to 20110919 snapshot (kde#282282 (OpenConnect), small UI improvements)

* Sun Sep 18 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.58.20110918git.nm09
- update to 20110918 snapshot, fixes #605527 (wired PPPoE) among other things

* Wed Sep 07 2011 Lukas Tinkl <ltinkl@redhat.com> - 1:0.9-0.57.20110907git.nm09
- update to current git nm09 snapshot, for details see: 
  http://lamarque-lvs.blogspot.com/2011/09/plasma-nm-bugs-fixed-after-470.html
- fix #605527: KNetworkManager can´t connect to DSL/PPPoE connection
- fix #715459: KDE's wireless broken on secure AP w/ "hidden" setup
- fix #715461: KDE's wireless broken on secure AP w/ manual entry

* Sun Aug 28 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.56.20110828git.nm09
- update to 20110828 snapshot, fixes kde#280913 (OpenConnect) among other things
- bump minimum required NM version to 0.9.0 as required by the new snapshot

* Fri Aug 26 2011 David Woodhouse <dwmw2@infradead.org> - 0.9-0.55.20110812git.nm09
- Build OpenConnect VPN support (#717250)

* Fri Aug 12 2011 Lukas Tinkl <ltinkl@redhat.com> - 0.9-0.54.20110812git.nm09
- update to current snapshot, for changes and fixes see 
  http://lamarque-lvs.blogspot.com/2011/07/plasma-nm-bugs-fixed-after-465.html

* Fri Jun 17 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9-0.53.20110616git.nm09
- 20110616 nm09 branch snapshot.

* Wed Jun 08 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9-0.52.20110608git.nm09
- 20110608 snapshot, includes automatic nm08 migration

* Mon Jun 06 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9-0.51.20110606git.nm09
- 20110606 snapshot, includes manual nm08 migration

* Wed Jun 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.50.20110601git.nm09
- 20110601 snapshot
- bump solid networkmanger09 priority

* Fri May 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.49.20110527git.nm09
- update to 20110527 snapshot from nm09 branch
- make it clear in Release where the snapshot comes from
- drop nm09 conditional, this version targets only NetworkManager 0.9

* Thu May 19 2011 Lukas Tinkl <ltinkl@redhat.com> - 1:0.9-0.48.20110519
- update to current snapshot from nm09 branch
- remove obsolete compat patch

* Sat Apr 30 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.47.20110323
- revert to the 20110323 snapshot (newer features not supported in F15)

* Wed Apr 20 2011 Lukas Tinkl <ltinkl@redhat.com> - 1:0.9-0.46.20110419
- fix VPN connections on the compat interface

* Tue Apr 19 2011 Lukas Tinkl <ltinkl@redhat.com> - 1:0.9-0.45.20110419
- update to current snapshot

* Sun Mar 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.44.20110323
- Restore the VPN subpackages, NM still ships VPN plugins separately

* Fri Mar 25 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.43.20110323
- Add Obsoletes/Provides for the dropped subpackages on F15+

* Fri Mar 25 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:0.9-0.42.20110323
- Conditionalize NM 0.9 (with compat patches) support to F15+
- Merge VPN subpackages into the main package for F15+ to match NM 0.9 packaging

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> 1:0.9-0.41.20110323
- Rebuild with NM 0.9 compat patch

* Wed Mar 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.40.20110323
- 20110323 snapshot
- BR: mobile-broadband-provider-info-devel

* Mon Mar 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.39.20110314
- 20110314 snapshot

* Mon Mar 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.38.20110310
- fix "In file (unencrypted)" secrets storage (#682972)

* Thu Mar 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.37.20110310
- 20110310 snapshot
- Updated code to fix "Enable ..." checkbox handling

* Tue Mar 08 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.36.20110308
- 20110308 snapshot

* Mon Feb 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.35.20110221
- 20110221 snapshot

* Thu Feb 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.34.20110217
- 20110217 snapshot (with translations)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-0.33.20110106
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.32.20110106
- 20110106 snapshot (sans translations for now)

* Wed Nov 17 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.31.20101117
- 20101117 snapshot
- "Always ask for password" does not work (#582933,kde#244416)

* Tue Nov 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.30.20101105
- move shared bits to main pkg
- -libs: Requires: %%name

* Tue Nov 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.29.20101105
- 20101105 snapshot
- use kde-plasma-networkmangement-* subpkg names
- drop monolithic/knm bits

* Fri Oct 22 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.28.20101011.2
- rebuild for kde-4.5

* Mon Oct 11 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.28.20101011
- 20101011 snapshot
- KDE NM applet 20101008 snapshot crashes on new CDMA connection (#641792)
- Add NetworkManager dependency to knetworkmanager (#618918)

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.27.20101008
- 20101008 snapshot, includes new Adding Mobile Connection Wizard (#584124)

* Wed Sep 29 2010 jkeating - 1:0.9-0.26.20100920
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.25.20100920
- make plasma_applet unconditional
- include javascript to enable nm plasmoid in systray, kde45+ (#604798)

* Mon Sep 20 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.24.20100920
- 20100920 snapshot
- Obsoletes: knetworkmanager , if built against kde-4.5 (#604798)

* Tue Sep 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.23.20100830
- knetworkmanager doesn´t recognize BSSID (kde#238046)

* Mon Aug 30 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.22.20100830
- 20100830 snapshot
- Requires: kdebase-runtime

* Tue Jun 29 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.21.20100603
- Conflicts: kdebase-runtime > 4.4.76 (if built on/for < kde-4.4)
- use -DINSTALL_KNM_AUTOSTART=ON (compat with f12's cmake)

* Thu Jun 03 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.20.20100603
- 20100603 snapshot
- Add "Enable networking" button to knetworkmanager (rh#598765,kde#238325)

* Mon Apr 19 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.19.20100419
- 20100419 snapshot

* Thu Apr 01 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.18.20100401
- 20100401 snapshot
- (re)add warning about plasma applet stability

* Fri Mar 19 2010 Jaroslav Reznik <jreznik@redhat.com> 1:0.9-0.17.20100310
- split out PPTP VPN ui to -pptp

* Wed Mar 10 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.16.20100310
- 20100310 kdereview snapshot
- vpn-related fixes/improvements to plasmoid

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.15.20100309
- move common items to -libs, make knm,-nm installable separately.

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.14.20100309
- 200100309 snapshot
- on queue, plasmoid reportedly ready for wider testing, re-enabling (#571433)

* Mon Mar 08 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.13.20100220svn
- make kde-plasma-neworkmanagment an empty placeholder package (#571433)
- knetworkmanager: move kcm_networkmanagement_tray bits here (from kde-plasma-nm)

* Sun Feb 21 2010 Kevin Kofler <Kevin@tigcc.ticalc.org>  1:0.9-0.12.20100220svn
- update to revision 1093233 (2010-02-20)
- use user-readable URL instead of outdated websvn link
- include translations (#566386, use create_tarball.rb script from kdesdk trunk)

* Wed Feb 10 2010 Kevin Kofler <Kevin@tigcc.ticalc.org>  1:0.9-0.11.20100210svn
- update to revision 1088283 (2010-02-10)
- drop F10 conditionals
- warn about the plasmoid being experimental, recommend knetworkmanager
- drop minimum version requirements for qt and kdelibs, not needed anymore

* Thu Jan 28 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.10.20091220svn
- -libs: use %%{_kde4_version}

* Mon Dec 21 2009 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.9.20091220svn
- 20091220 snapshot
- -libs: use/tighten qt4/kdelibs4 deps

* Tue Nov 24 2009 Rex Dieter <rdieter@fedoraproject.org> 1:0.9-0.8.20091124svn
- New snapshot
- BR: qt4-devel >= 4.6.0

* Tue Nov 24 2009 Ben Boeckel <MathStuf@gmail.com> - 1:0.9-0.7.20091024svn
- Rebuild for Qt 4.6b1 ABI break

* Sun Oct 25 2009 Ben Boeckel <MathStuf@gmail.com> 1:0.9-0.6.20091024svn
- Rebuild with new sources

* Sun Oct 25 2009 Ben Boeckel <MathStuf@gmail.com> 1:0.9-0.5.20091024svn
- New snapshot

* Sun Oct 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org>  1:0.9-0.4.20090930svn
- Build as knetworkmanager4 for F10 so KDE 3 KNM users are not forced to upgrade
- Obsolete knetworkmanager4 (and keep replacing the KDE 3 KNM) on F11+

* Wed Sep 30 2009 Ben Boeckel <MathStuf@gmail.com> 1:0.9-0.3.20090930svn
- New snapshot

* Mon Sep 21 2009 Ben Boeckel <MathStuf@gmail.com> 1:0.9-0.2.20090919svn
- Add back missing Requires:

* Mon Sep 21 2009 Ben Boeckel <MathStuf@gmail.com> 1:0.9-0.1.20090919svn
- Version seems to be .9 now
- Fix trailing spaces
- New snapshot

* Tue Sep 15 2009 Rex Dieter <rdieter@fedoraproject.org> 1:0.8-0.22.20090815svn
- Epoch: 1

* Fri Aug 28 2009 Rex Dieter <rdieter@fedoraproject.org> 0.8-0.21.20090815svn
- use knetworkmanager pkg names
- quasi-artificially inflate version to 0.8 (for now), to simplify upgrade path
  for knetworkmanager-0.7 (from F-10)
- nuke -devel pkg
- drop references to short-lived kde-plasma-networkmanager

* Sat Aug 15 2009 Rex Dieter <rdieter@fedoraproject.org> 0.1-0.20.20090815svn
- New snapshot
- optimize scriptlets
- -libs subpkg, multilib-friendly

* Mon Jul 27 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.19.20090726svn
- Add BR on kdelibs-experimental-devel

* Mon Jul 27 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.18.20090726svn
- New snapshot

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.17.20090602svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Rex Dieter <rdieter@fedoraproject.org> 0.1-0.16.20090602svn
- Requires: NetworkManager

* Wed Jun 03 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.15.20090602svn
- Remove patch and use wildcards instead

* Wed Jun 03 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.14.20090602svn
- New snapshot (revision 976742 committed 2009-06-02 13:47 UTC)

* Thu May 21 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.1-0.13.20090519svn
- Give the internal libs sonames independent of the KDE version (fix F12 build)

* Wed May 20 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.12.20090519svn
- New snapshot (revision 970021 committed 2009-05-19 13:34 UTC)

* Tue May 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.1-0.11.20090504svn
- New snapshot (revision 963263 committed 2009-05-04 10:57 UTC)
- Clarify %%description

* Fri Apr 24 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.10.20090424svn
- Respin snapshot
- Add disclaimer to %%description

* Wed Apr 8 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.9.20090403svn
- Respin snapshot

* Tue Mar 3 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.8.20090302svn
- Respin snapshot

* Tue Mar 3 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.1-0.7.20090217svn
- Obsoletes/Provides knetworkmanager on F11+ for upgrade paths

* Tue Feb 24 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.6.20090217svn
- Moved P/O to correct places

* Sat Feb 21 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.5.20090217svn
- Fixed Provides to have a version
- Fixed Obsoletes/Provides for subpackages
- Fixed licensing

* Fri Feb 20 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.4.20090217svn
- Fixed Obsoletes/Provides
- Fixed URL

* Sat Feb 7 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.3.20090207svn
- Add changelog
- Added tarball creation
- Changed name to kde-plasma-networkmanagement

* Tue Jan 13 2009 Rex Dieter <rdieter[AT]fedoraproject.org> 0.1-0.2.20090111svn
- General cleanup

* Sun Jan 11 2009 Ben Boeckel <MathStuf@gmail.com> 0.1-0.1.20090111svn
- Initial package
