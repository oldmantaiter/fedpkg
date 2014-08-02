Summary:  An open-source mapreduce framework.
Name: disco
Version: 0.5.3
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemon
URL: http://www.discoproject.org
Source0: disco.tar.gz
BuildRoot: %{_tmppath}/disco-%{version}-root
Vendor: Disco Authors

%description
Disco is a lightweight, open-source framework for distributed computing based
on the MapReduce paradigm.

Disco is powerful and easy to use, thanks to Python. Disco distributes and
replicates your data, and schedules your jobs efficiently. Disco even includes
the tools you need to index billions of data points and query them in
real-time.

%package master
Summary: Disco Master
Group: System Environment/Daemon
Requires: erlang
Requires: python-%{name} == %{version}-%{release}
Requires: %{name}-cli == %{version}-%{release}
BuildRequires: erlang erlang-rebar git

%description master
This package contains the required files to run the disco master

%package node
Summary: Disco Node
Group: System Environment/Daemon
Requires: erlang
Requires: python-%{name} == %{version}-%{release}
BuildRequires: erlang erlang-rebar git

%description node
This package contains the required files to run the disco node

%package -n python-%{name}
Summary: Disco Python Libs
Group: Development/Languages
Requires: python2
BuildRequires: python2-devel, python-setuptools

%description -n python-%{name}
This package contains the disco python libraries for Python

%package cli
Summary: Disco CLI Utilities
Group: Development/Tools
Requires: python2
Requires: python-%{name} = %{version}-%{release}

%description cli
This package contains the disco command-line tools ddfs and disco

%prep
%setup -n disco

%build
%{__make} fedpkg REBAR=rebar

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT REBAR=rebar
%{__make} install-node DESTDIR=$RPM_BUILD_ROOT REBAR=rebar

# Cleanup from Makefile doing auto python install
rm -rf $RPM_BUILD_ROOT/%{_prefix}/lib/python*

# Explicitely do the python install ourselves
cd lib
DISCO_VERSION=%{version}  %{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT

cd ../
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin
cp bin/disco bin/ddfs $RPM_BUILD_ROOT/%{_prefix}/bin

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files master
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/disco/settings.py
%dir /etc/disco
%dir %{_prefix}/var/disco
%dir %{_prefix}/lib/disco
%dir %{_prefix}/share/disco
%{_prefix}/lib/disco/*
%{_prefix}/share/disco/*

%files node
%defattr(-,root,root)
%dir %{_prefix}/var/disco
%dir %{_prefix}/lib/disco
%{_prefix}/lib/disco/*

%files -n python-%{name}
%defattr(-,root,root)
%{python2_sitelib}/clx/
%{python2_sitelib}/disco/
%{python2_sitelib}/disco-*.egg-info

%files cli
%defattr(-,root,root)
%attr(0755,root,root) %{_prefix}/bin/disco
%attr(0755,root,root) %{_prefix}/bin/ddfs


%changelog
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
