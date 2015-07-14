%global upstream_name brewer2mpl

Name: python-%{upstream_name}
Version: 1.4.1
Release: 1%{?dist}
Summary: A pure Python package for accessing colorbrewer2.org color maps from Python

License: MIT

URL: https://github.com/jiffyclub/%{upstream_name}/
Source0: https://pypi.python.org/packages/source/b/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel python-setuptools

%description
With brewer2mpl you can get the raw RGB colors of all 165 colorbrewer2.org color maps.
The color map data ships with brewer2mpl so no internet connection is required.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root %{buildroot}

%files
%doc README.rst
%{python2_sitelib}/%{upstream_name}*

%changelog
* Fri Jul 10 2015 Tait Clarridge <tait@clarridge.ca> - 1.4.1-1
- Initial specfile
