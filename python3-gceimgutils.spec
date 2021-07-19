#
# spec file for package python3-gceimgutils
#
# Copyright (c) 2018 SUSE Linux GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define upstream_name gceimgutils

%bcond_without test
Name:           python3-gceimgutils
Version:        0.10.0
Release:        0
Summary:        Image management utilities for GCE
License:        GPL-3.0+
Group:          System/Management
Url:            https://github.com/SUSE-Enceladus/gceimgutils
Source0:        %{upstream_name}-%{version}.tar.bz2
Requires:       python3
Requires:       python3-google-api-python-client
Requires:       python3-google-auth
Requires:       python3-google-cloud-core
Requires:       python3-google-cloud-storage
BuildRequires:  python3-google-api-python-client
BuildRequires:  python3-google-auth
BuildRequires:  python3-google-cloud-core
BuildRequires:  python3-google-cloud-storage
%if %{with test}
BuildRequires:  python3-pytest
%endif
BuildRequires:  python3-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
A collection of image manipulation utilities for GCE. These include:
gceremoveimg: Removes images from GCE

%prep
%setup -q -n %{upstream_name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -m 644 man/man1/* %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{_mandir}/man1/*

%check
%if %{with test}
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
python3 -m pytest
%endif

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_mandir}/man*/*
%dir %{python3_sitelib}/gceimgutils
%{python3_sitelib}/*
%{_bindir}/*

%changelog
