%global upname ggplot

Name: python-%{upname}
Version: 0.6.5
Release: 1%{?dist}
Summary: A Python port of the R package ggplot2

License: BSD

URL: https://github.com/yhat/ggplot/
Source0: https://pypi.python.org/packages/source/g/ggplot/ggplot-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-statsmodels
Requires: numpy scipy python-pandas python-statsmodels python-matplotlib python-brewer2mpl

%description
It's an extremely un-pythonic package for doing exactly what ggplot2
does. The goal of the package is to mimic the ggplot2 API. This makes it
super easy for people coming over from R to use, and prevents you
from having to re-learn how to plot stuff.

%prep
%setup -q -n %{upname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root %{buildroot}

%files
%doc README.rst
%{python2_sitelib}/%{upname}*

%changelog
* Fri Jul 10 2015 Tait Clarridge <tait@clarridge.ca> - 0.6.5-1
- Update to 0.6.5
- Add brewer2mpl requirement

* Wed Jan 15 2014 Sergio Pascual <sergio.pasra@gmail.com> - 0.4.5-1
- Initial specfile
