# Disable debug packages - useless for this package
%global debug_package %{nil}

Summary:  An open-source mapreduce framework
Name: disco
Version: 0.5.3
Release: 1%{?dist}
License: BSD
URL: http://www.discoproject.org
Source0: disco.tar.gz

%description
Disco is a lightweight, open-source framework for distributed computing based
on the MapReduce paradigm.

Disco is powerful and easy to use, thanks to Python. Disco distributes and
replicates your data, and schedules your jobs efficiently. Disco even includes
the tools you need to index billions of data points and query them in
real-time.

%package -n erlang-%{name}
Summary: Disco Erlang Files
License: BSD
Requires: erlang
Requires: python-%{name} == %{version}-%{release}
BuildRequires: erlang erlang-rebar git

%description -n erlang-%{name}
Contains the erlang files for disco

%package master
Summary: Disco Master
License: BSD
Requires: erlang-%{name} == %{version}-%{release}
Requires: python-%{name} == %{version}-%{release}
Requires: %{name}-cli == %{version}-%{release}
Requires: systemd
BuildRequires: systemd

%description master
This package contains the required files to run the disco master

%package -n python-%{name}
Summary: Disco Python Libs
License: BSD
Requires: python2
BuildRequires: python2-devel, python-setuptools

%description -n python-%{name}
This package contains the disco python libraries for Python

%package cli
Summary: Disco CLI Utilities
License: BSD
Requires: python2
Requires: python-%{name} = %{version}-%{release}
BuildRequires:  python-sphinx

%description cli
This package contains the disco command-line tools ddfs and disco

%prep
%setup -q -n disco

%build
make fedpkg REBAR=rebar

%install

# Cleanup from Makefile doing auto python install
rm -rf %{buildroot}%{_prefix}/lib/python*

# Explicitely do the python install ourselves
pushd lib
DISCO_VERSION=%{version}  %{__python2} setup.py install -O1 --root=%{buildroot}
popd

mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 bin/disco %{buildroot}%{_bindir}/disco
install -p -m 0755 bin/ddfs %{buildroot}%{_bindir}/ddfs

mkdir -p %{buildroot}%{_libdir}/erlang/lib/disco-%{version}/master/{deps,ebin}

%define _erl_build_base %{buildroot}%{_libdir}/erlang/lib/disco-%{version}

# Do deps first
for d in master/deps/*; do
    base="$(basename "$d")"
    install_base="%{_erl_build_base}/master/deps/$base/ebin"
    #install -p -m 0755 -d "$install_base"
    for f in master/deps/$base/ebin/*; do
        install -p -D -m 0644 $f $install_base/$(basename "$f")
    done
done

# Install disco
for f in master/ebin/*; do
    install -p -m 0644 $f %{_erl_build_base}/master/ebin/$(basename "$f")
done

## Install headers - disabled
#mkdir -p %{buildroot}%{_libdir}/erlang/lib/disco-%{version}/include/{disco,ddfs}
#for hf in master/include/*; do
#    install -p -m 0644 $hf %{_erl_build_base}/include/$(basename "$hf")
#done

#for ddfs_h in master/src/ddfs/*.hrl; do
#    install -p -m 0644 $ddfs_h %{_erl_build_base}/include/ddfs/$(basename "$ddfs_h")
#done

#for disco_h in master/src/*.hrl; do
#    install -p -m 0644 $disco_h %{_erl_build_base}/include/disco/$(basename "$disco_h")
#done

# Install WWW files
install -p -m 0755 -d "%{buildroot}%{_datadir}/disco"
cp -r master/www %{buildroot}%{_datadir}/disco

# Install settings
pushd conf
ABSTARGETLIB="%{_libdir}/erlang/lib/disco-%{version}" ABSTARGETSRV="unset" ABSTARGETDAT="%{_datadir}/disco" WWW="www" ./gen.settings.sh > settings.py
install -p -D -m 0644 settings.py %{buildroot}%{_sysconfdir}/disco/settings.py.example
popd

# Install systemd file
install -p -D -m 0644 contrib/systemd/disco.service %{buildroot}%{_unitdir}/%{name}.service

# Install docs for ddfs and disco commands
pushd doc
SPHINXOPTS="-D version=%{version} -D release=%{version}" make man -e
install -p -D -m 0644 .build/man/ddfs.1 %{buildroot}%{_mandir}/man1/ddfs.1
gzip %{buildroot}%{_mandir}/man1/ddfs.1
install -p -D -m 0644 .build/man/disco.1 %{buildroot}%{_mandir}/man1/disco.1
gzip %{buildroot}%{_mandir}/man1/disco.1
popd

# TODO: create a HOWTO configure once installed and put it in %{_datadir}/disco/docs

%files -n erlang-%{name}
%dir %{_libdir}/erlang/lib/disco-*
%{_libdir}/erlang/lib/disco-*/master/ebin
%{_libdir}/erlang/lib/disco-*/master/deps
# Headers can be included, but they will probably not prove useful
#%{_libdir}/erlang/lib/disco-*/include/

%files master
%defattr(-,root,root)
# Config file
%dir %{_sysconfdir}/disco
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/disco/settings.py.example
# Systemd file
%{_unitdir}/%{name}.service
# WWW files for master
%{_datadir}/disco/

%files -n python-%{name}
%defattr(-,root,root)
%{python2_sitelib}/clx/
%{python2_sitelib}/disco/
%{python2_sitelib}/disco-*.egg-info

%files cli
%defattr(-,root,root)
%{_mandir}/man1/disco.1.gz
%{_mandir}/man1/ddfs.1.gz
%{_bindir}/disco
%{_bindir}/ddfs


%changelog
* Tue Aug 05 2014 Tait Clarridge <tait@clarridge.ca> - 0.5.3-1
- More fixes for Fedora packaging guidelines
- Removed erlang files from master/node package and made it erlang-disco for Erlang packaging
- Removed disco-node and replaced with erlang-disco
- Added documentation for disco/ddfs commands

* Sat Aug 02 2014 Tait Clarridge <tait@clarridge.ca> - 0.5.3-1
- Removing generic paths from the Makefile and general fixups for packaging guidelines

* Fri Aug 01 2014 Tait Clarridge <tait@clarridge.ca> - 0.5.3-1
- Removing packager for submission to Fedora and EPEL

* Fri Aug 01 2014 Shayan Pooya <shayan@liveve.org> - 0.5.3-1
- Release version 0.5.3

* Thu Jun 05 2014 Shayan Pooya <shayan@liveve.org> - 0.5.2-1
- Release version 0.5.2

* Wed Apr 16 2014 Shayan Pooya <shayan@liveve.org> - 0.5.1-1
- Release version 0.5.1

* Wed Apr 02 2014 Shayan Pooya <shayan@liveve.org> - 0.5.0-1
- Initial packaging
- Make python-disco a dependency of node and master subpackages
