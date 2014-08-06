# Disabled - the erlang package already is compiled with debug_info by rebar
%global debug_package %{nil}

Summary:  An open-source map-reduce framework
Name: disco
Version: 0.5.3
Release: 1%{?dist}
License: BSD
URL: http://www.discoproject.org
# Disco requires the cloned git repo for rebar to get the version from the gitlog
# git clone https://github.com/discoproject/disco
# git checkout 0.5.3
Source0: disco.tar.gz
Requires: erlang >= R16B
Requires: python-%{name} == %{version}-%{release}
BuildRequires: erlang erlang-rebar git

%description
Disco is a lightweight, open-source framework for distributed computing based
on the Map-Reduce paradigm.

Disco is powerful and easy to use, thanks to Python. Disco distributes and
replicates your data, and schedules your jobs efficiently. Disco even includes
the tools you need to index billions of data points and query them in
real-time.

This package installs the Erlang components for disco slave/master to run.

%package master
Summary: Disco master web and service files
License: BSD
Requires: %{name}%{?_isa} == %{version}-%{release}
Requires: %{name}-cli == %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description master
This package contains the required files to run the Disco master

%package -n python-%{name}
Summary: Disco Python Libs
License: BSD
Requires: python2
BuildRequires: python2-devel python-setuptools
BuildRequires: gzip

%description -n python-%{name}
This package contains the Disco python libraries

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
make %{?_smp_mflags} fedpkg REBAR=rebar

%install

# Python install
pushd lib
DISCO_VERSION=%{version}  %{__python2} setup.py install -O1 --root=%{buildroot}
popd

# CLI utils install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0755 bin/ddfs %{buildroot}%{_bindir}/ddfs

%global _erl_build_base %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}

# Install disco dependencies
for d in master/deps/*; do
    base="$(basename "$d")"
    install_base="%{_erl_build_base}/master/deps/$base/ebin"
    for f in master/deps/$base/ebin/*; do
        install -p -D -m 0644 $f $install_base/$(basename "$f")
    done
done

# Install disco
for f in master/ebin/*; do
    install -p -D -m 0644 $f %{_erl_build_base}/master/ebin/$(basename "$f")
done

# Install WWW files for master
for f in master/www/*; do
    if [ -d $f ]; then
        for g in master/www/$(basename "$f")/*; do
            install -p -D -m 0644 $g %{buildroot}%{_datadir}/%{name}/www/$(basename "$f")/$(basename "$g")
        done
    else
        install -p -D -m 0644 $f %{buildroot}%{_datadir}/%{name}/www/$(basename "$f")
    fi
done

# Install settings for master
pushd conf
ABSTARGETLIB="%{_libdir}/erlang/lib/%{name}-%{version}" ABSTARGETSRV="unset" ABSTARGETDAT="%{_datadir}/%{name}" WWW="www" ./gen.settings.sh > settings.py
install -p -D -m 0644 settings.py %{buildroot}%{_sysconfdir}/%{name}/settings.py.example
popd

# Install systemd file for master
install -p -D -m 0644 contrib/systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service

# Install docs for ddfs and disco commands
pushd doc
SPHINXOPTS="-D version=%{version} -D release=%{version}" make man -e
install -p -D -m 0644 .build/man/ddfs.1 %{buildroot}%{_mandir}/man1/ddfs.1
gzip %{buildroot}%{_mandir}/man1/ddfs.1
install -p -D -m 0644 .build/man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
gzip %{buildroot}%{_mandir}/man1/%{name}.1
popd

%files
%doc LICENSE
%dir %{_libdir}/erlang/lib/%{name}-*
%dir %{_libdir}/erlang/lib/%{name}-*/master
%{_libdir}/erlang/lib/%{name}-*/master/ebin
%{_libdir}/erlang/lib/%{name}-*/master/deps

%files master
%dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/settings.py.example
%{_unitdir}/%{name}.service
%{_datadir}/%{name}/

%files -n python-%{name}
%doc LICENSE
%{python2_sitelib}/clx/
%{python2_sitelib}/%{name}/
# Fix some rpmlint errors - disco sets these as executable in the jobhome directory anyways
%attr(755, root, root) %{python2_sitelib}/%{name}/worker/__init__.py
%attr(755, root, root) %{python2_sitelib}/%{name}/worker/simple.py
%attr(755, root, root) %{python2_sitelib}/%{name}/worker/classic/worker.py
%attr(755, root, root) %{python2_sitelib}/%{name}/worker/pipeline/worker.py
%{python2_sitelib}/%{name}-*.egg-info

%files cli
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/ddfs.1.gz
%{_bindir}/%{name}
%{_bindir}/ddfs

%post -n %{name}-master
%systemd_post %{name}.service

%preun -n %{name}-master
%systemd_preun %{name}.service

%postun -n %{name}-master
%systemd_postun_with_restart %{name}.service 

%check
rebar eunit skip_deps=true -v

%changelog
* Tue Aug 05 2014 Tait Clarridge <tait@clarridge.ca> - 0.5.3-1
- Initial build
